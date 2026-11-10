"""Module for reading and standardizing agricultural foreign trade data from MAG (Ecuador)."""

import os
import pandas as pd
from typing import Dict, Any, Optional


class MAGReader:
    """Reader for MAG Foreign Trade Excel dataset (mag_comercioexterior_2026octubre.xlsx)."""

    def __init__(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"MAG data file not found: {file_path}")
        self.file_path = file_path
        self.sheet_name = "MAG_CE_2026Octubre"
        self._raw_df: Optional[pd.DataFrame] = None

    def load_data(self) -> pd.DataFrame:
        """Loads and caches raw Excel data."""
        if self._raw_df is None:
            self._raw_df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
        return self._raw_df.copy()

    def get_standardized_data(self) -> pd.DataFrame:
        """Returns standardized MAG data with clear metric units:

        - weight in metric tons (TM) and kg.
        - values in USD (converted from thousands of USD).
        - unit price FOB (USD/kg).
        - separates annual data from partial periods.
        """
        df = self.load_data()

        # Clean string columns
        df["CE_PRODUCTO"] = df["CE_PRODUCTO"].astype(str).str.strip()
        df["CE_PERIODO"] = df["CE_PERIODO"].astype(str).str.strip()
        df["CE_ANIO"] = df["CE_ANIO"].astype(int)

        # Standardize numeric columns
        for col in ["CE_EXP_PESO", "CE_EXP_VALOR", "CE_IMP_PESO", "CE_IMP_VALOR"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

        # Explicit unit conversion
        # MAG units: Weight in Metric Tons, Value in Thousands of USD
        df["export_weight_mt"] = df["CE_EXP_PESO"]
        df["export_weight_kg"] = df["CE_EXP_PESO"] * 1000.0
        df["export_value_usd"] = df["CE_EXP_VALOR"] * 1000.0

        df["import_weight_mt"] = df["CE_IMP_PESO"]
        df["import_weight_kg"] = df["CE_IMP_PESO"] * 1000.0
        df["import_value_usd"] = df["CE_IMP_VALOR"] * 1000.0

        # Unit price FOB (USD/kg) = export_value_usd / export_weight_kg = CE_EXP_VALOR / CE_EXP_PESO
        df["unit_price_fob_usd_kg"] = df.apply(
            lambda row: (row["export_value_usd"] / row["export_weight_kg"])
            if row["export_weight_kg"] > 0
            else 0.0,
            axis=1,
        )

        df["is_partial_year"] = df["CE_PERIODO"] != "Enero - Diciembre"
        df["source"] = "MAG_Ecuador"

        return df

    def get_series_by_product(
        self, product_name: str, annual_only: bool = True
    ) -> pd.DataFrame:
        """Filters data for a given product (e.g., 'Piña', 'Pitahaya')."""
        df = self.get_standardized_data()
        subset = df[df["CE_PRODUCTO"].str.lower() == product_name.lower()].copy()
        if annual_only:
            subset = subset[~subset["is_partial_year"]]
        return subset.sort_values("CE_ANIO").reset_index(drop=True)

    def get_reconciliation_benchmarks(self, year: int = 2025) -> Dict[str, Any]:
        """Returns benchmarks forconciliation controls (2025 values)."""
        df = self.get_standardized_data()
        subset = df[(df["CE_ANIO"] == year) & (~df["is_partial_year"])]

        benchmarks = {}
        for _, row in subset.iterrows():
            prod = row["CE_PRODUCTO"]
            benchmarks[prod] = {
                "year": year,
                "weight_mt": float(row["export_weight_mt"]),
                "weight_kg": float(row["export_weight_kg"]),
                "value_usd": float(row["export_value_usd"]),
                "unit_price_usd_kg": float(row["unit_price_fob_usd_kg"]),
                "period": row["CE_PERIODO"],
            }
        return benchmarks
