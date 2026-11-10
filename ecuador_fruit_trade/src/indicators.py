"""Economic and Trade Intelligence Indicators for Fruit Trade Analysis."""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional


def calculate_market_share(
    value_dest: float, total_value: float
) -> Optional[float]:
    """Calculates market share percentage (exportaciones_destino / exportaciones_totales * 100)."""
    if total_value and total_value > 0:
        return (value_dest / total_value) * 100.0
    return None


def calculate_unit_price(value_usd: float, weight_kg: float) -> Optional[float]:
    """Calculates FOB unit price in USD per kg."""
    if weight_kg and weight_kg > 0 and value_usd and value_usd > 0:
        return value_usd / weight_kg
    return None


def calculate_yoy_growth(current_val: float, prev_val: float) -> Optional[float]:
    """Calculates Year-over-Year growth percentage ((valor_t / valor_t_anterior - 1) * 100)."""
    if prev_val and prev_val > 0:
        return ((current_val / prev_val) - 1.0) * 100.0
    return None


def calculate_cagr(
    initial_val: float, final_val: float, num_years: int
) -> Optional[float]:
    """Calculates Compound Annual Growth Rate (CAGR = (V_f / V_0)**(1/n) - 1)."""
    if initial_val and initial_val > 0 and final_val and final_val > 0 and num_years > 0:
        return ((final_val / initial_val) ** (1.0 / num_years) - 1.0) * 100.0
    return None


def calculate_ecuador_penetration(
    imports_from_ecuador: float, total_market_imports: float
) -> Optional[float]:
    """Calculates Ecuador market penetration rate ((imports_from_ecu / total_imports) * 100)."""
    if total_market_imports and total_market_imports > 0:
        return (imports_from_ecuador / total_market_imports) * 100.0
    return None


def calculate_hhi(shares_pct: List[float]) -> float:
    """Calculates Herfindahl-Hirschman Index (HHI = sum(s_i^2)) using percentages (0-100).

    Range: 0 to 10,000.
    - HHI < 1,500: Unconcentrated / Diversified
    - 1,500 <= HHI <= 2,500: Moderately Concentrated
    - HHI > 2,500: Highly Concentrated
    """
    valid_shares = [s for s in shares_pct if s is not None and not np.isnan(s)]
    return float(sum(s**2 for s in valid_shares))


def calculate_cr3(shares_pct: List[float]) -> float:
    """Calculates Concentration Ratio of Top 3 destinations (CR3)."""
    valid_shares = sorted(
        [s for s in shares_pct if s is not None and not np.isnan(s)], reverse=True
    )
    return float(sum(valid_shares[:3]))


def calculate_market_metrics(destinations_df: pd.DataFrame) -> Dict[str, Any]:
    """Computes comprehensive destination concentration and distribution indicators.

    Requires columns: ['partner_name', 'primary_value_usd'] with partner != 'World'.
    """
    df = destinations_df[
        destinations_df["partner_name"].str.lower() != "world"
    ].copy()
    if df.empty:
        return {}

    total_val = df["primary_value_usd"].sum()
    if total_val == 0:
        return {}

    df["share_pct"] = (df["primary_value_usd"] / total_val) * 100.0
    df = df.sort_values("share_pct", ascending=False).reset_index(drop=True)

    shares = df["share_pct"].tolist()
    hhi = calculate_hhi(shares)
    cr3 = calculate_cr3(shares)
    top1_share = shares[0] if shares else 0.0
    top1_partner = df.iloc[0]["partner_name"] if not df.empty else "None"

    # Historical variability if series available
    cv = (
        float(df["primary_value_usd"].std() / df["primary_value_usd"].mean())
        if df["primary_value_usd"].mean() > 0
        else 0.0
    )

    concentration_level = "Diversificado"
    if hhi > 2500:
        concentration_level = "Altamente Concentrado"
    elif hhi >= 1500:
        concentration_level = "Moderadamente Concentrado"

    return {
        "total_export_usd": total_val,
        "num_destinations": len(df),
        "hhi": round(hhi, 2),
        "cr3_pct": round(cr3, 2),
        "top1_partner": top1_partner,
        "top1_share_pct": round(top1_share, 2),
        "concentration_level": concentration_level,
        "coefficient_of_variation": round(cv, 3),
    }
