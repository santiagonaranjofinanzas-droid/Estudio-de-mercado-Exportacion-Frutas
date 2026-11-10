"""Transformation and consolidation engine for Ecuador Fruit Trade Intelligence."""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from .indicators import (
    calculate_market_share,
    calculate_unit_price,
    calculate_yoy_growth,
    calculate_cagr,
    calculate_market_metrics,
)


class TradeTransformer:
    """Consolidates and structures trade datasets across MAG, Comtrade, and WITS."""

    def __init__(self, products_config: Dict[str, Any]):
        self.config = products_config

    def process_mag_history(self, mag_df: pd.DataFrame) -> pd.DataFrame:
        """Processes historical MAG trade series into standard format with growth metrics."""
        records = []
        for prod_key, prod_info in self.config.get("products", {}).items():
            mag_name = prod_info.get("mag_name")
            if not mag_name:
                continue

            sub = mag_df[
                (mag_df["CE_PRODUCTO"].str.lower() == mag_name.lower())
                & (~mag_df["is_partial_year"])
            ].sort_values("CE_ANIO")

            prev_val = None
            initial_val = sub.iloc[0]["export_value_usd"] if not sub.empty else None
            initial_year = sub.iloc[0]["CE_ANIO"] if not sub.empty else None

            for _, row in sub.iterrows():
                val = row["export_value_usd"]
                wt_kg = row["export_weight_kg"]
                yr = int(row["CE_ANIO"])

                yoy = calculate_yoy_growth(val, prev_val) if prev_val else None
                cagr = (
                    calculate_cagr(initial_val, val, yr - initial_year)
                    if (initial_val and yr > initial_year)
                    else None
                )

                records.append(
                    {
                        "source": "MAG_Ecuador",
                        "product_id": prod_key,
                        "product_name": prod_info.get("name_es"),
                        "hs6_code": prod_info.get("hs6"),
                        "year": yr,
                        "period": row["CE_PERIODO"],
                        "export_value_usd": val,
                        "export_weight_mt": row["export_weight_mt"],
                        "export_weight_kg": wt_kg,
                        "unit_price_usd_kg": row["unit_price_fob_usd_kg"],
                        "yoy_growth_pct": round(yoy, 2)
                        if yoy is not None
                        else None,
                        "cagr_from_start_pct": round(cagr, 2)
                        if cagr is not None
                        else None,
                    }
                )
                prev_val = val

            # Also add 2026 partial period if exists
            partial_sub = mag_df[
                (mag_df["CE_PRODUCTO"].str.lower() == mag_name.lower())
                & (mag_df["is_partial_year"])
            ]
            for _, row in partial_sub.iterrows():
                records.append(
                    {
                        "source": "MAG_Ecuador (Parcial)",
                        "product_id": prod_key,
                        "product_name": prod_info.get("name_es"),
                        "hs6_code": prod_info.get("hs6"),
                        "year": int(row["CE_ANIO"]),
                        "period": row["CE_PERIODO"],
                        "export_value_usd": row["export_value_usd"],
                        "export_weight_mt": row["export_weight_mt"],
                        "export_weight_kg": row["export_weight_kg"],
                        "unit_price_usd_kg": row["unit_price_fob_usd_kg"],
                        "yoy_growth_pct": None,  # Not comparable with full year
                        "cagr_from_start_pct": None,
                    }
                )

        return pd.DataFrame(records)

    def process_comtrade_destinations(
        self, comtrade_exports_df: pd.DataFrame, year: int = 2025
    ) -> pd.DataFrame:
        """Processes Comtrade export data to extract Top destinations and market shares."""
        if comtrade_exports_df.empty:
            return pd.DataFrame()

        df_year = comtrade_exports_df[
            (comtrade_exports_df["period"] == year)
            & (comtrade_exports_df["partner_name"].str.lower() != "world")
        ].copy()

        processed_dfs = []
        for cmd_code, group in df_year.groupby("cmd_code"):
            total_val = group["primary_value_usd"].sum()
            group = group.sort_values(
                "primary_value_usd", ascending=False
            ).reset_index(drop=True)
            group["ranking"] = group.index + 1
            group["share_pct"] = group["primary_value_usd"].apply(
                lambda v: calculate_market_share(v, total_val)
            )

            # Assign product info
            prod_info = next(
                (
                    v
                    for v in self.config.get("products", {}).values()
                    if v.get("hs6") == cmd_code
                ),
                {},
            )
            group["product_id"] = prod_info.get("id", cmd_code)
            group["product_name"] = prod_info.get("name_es", cmd_code)
            group["coverage_notes"] = prod_info.get("notes", "")

            processed_dfs.append(group)

        if not processed_dfs:
            return pd.DataFrame()

        result = pd.concat(processed_dfs, ignore_index=True)
        return result

    def get_top_destinations_summary(
        self, destinations_df: pd.DataFrame, top_n: int = 10
    ) -> pd.DataFrame:
        """Filters top N destinations per product."""
        if destinations_df.empty:
            return pd.DataFrame()
        return (
            destinations_df.groupby("cmd_code")
            .apply(lambda grp: grp.nsmallest(top_n, "ranking"))
            .reset_index(drop=True)
        )
