"""Unit and Integration Tests for Ecuador Fruit Trade Pipeline."""

import os
import sys

# Ensure ecuador_fruit_trade package root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import pandas as pd
import numpy as np

from src.mag_reader import MAGReader
from src.indicators import (
    calculate_market_share,
    calculate_unit_price,
    calculate_yoy_growth,
    calculate_cagr,
    calculate_ecuador_penetration,
    calculate_hhi,
    calculate_cr3,
    calculate_market_metrics,
)
from src.comtrade_client import UNComtradeClient
from src.validation import TradeValidator


@pytest.fixture
def base_dir():
  return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_indicators_math():
  """Tests economic and concentration formula calculations."""
  # Market share
  assert calculate_market_share(25, 100) == 25.0
  assert calculate_market_share(0, 100) == 0.0
  assert calculate_market_share(50, 0) is None

  # Unit price
  assert calculate_unit_price(1000.0, 500.0) == 2.0
  assert calculate_unit_price(0.0, 500.0) is None

  # YoY growth
  assert pytest.approx(calculate_yoy_growth(110.0, 100.0), 0.0001) == 10.0
  assert pytest.approx(calculate_yoy_growth(80.0, 100.0), 0.0001) == -20.0
  assert calculate_yoy_growth(100.0, 0.0) is None

  # CAGR: 100 to 200 in 2 years -> sqrt(2) - 1 ≈ 41.42%
  cagr = calculate_cagr(100.0, 200.0, 2)
  assert pytest.approx(cagr, 0.01) == 41.42

  # HHI and CR3
  # Shares: 50%, 30%, 20% -> HHI = 2500 + 900 + 400 = 3800
  shares = [50.0, 30.0, 20.0]
  assert calculate_hhi(shares) == 3800.0
  assert calculate_cr3(shares) == 100.0


def test_mag_reader(base_dir):
  """Tests MAG reader, unit conversions and 2025 benchmark reconciliation values."""
  mag_file = os.path.join(
      base_dir, "data", "raw", "mag_comercioexterior_2026octubre.xlsx"
  )
  reader = MAGReader(mag_file)
  benchmarks = reader.get_reconciliation_benchmarks(2025)

  # Piña 2025 benchmark: ~$81,108,645.51
  pina = benchmarks.get("Piña")
  assert pina is not None
  assert pytest.approx(pina["value_usd"], 1.0) == 81108645.51
  assert pytest.approx(pina["weight_mt"], 1.0) == 140448.025

  # Pitahaya 2025 benchmark: ~$272,762,184.80
  pita = benchmarks.get("Pitahaya")
  assert pita is not None
  assert pytest.approx(pita["value_usd"], 1.0) == 272762184.80
  assert pytest.approx(pita["weight_mt"], 1.0) == 64499.825


def test_comtrade_partner_resolution(base_dir):
  """Tests resolution of numerical country codes to names and ISO codes."""
  partner_file = os.path.join(base_dir, "data", "raw", "partnerAreas.json")
  client = UNComtradeClient(
      raw_storage_dir=os.path.join(base_dir, "data", "raw", "comtrade"),
      partner_areas_file=partner_file,
  )

  res_world = client.resolve_partner(0)
  assert res_world["partner_name"] == "World"

  res_ecu = client.resolve_partner(218)
  assert res_ecu["partner_name"] == "Ecuador"

  res_usa = client.resolve_partner(842)
  assert res_usa["partner_name"] == "USA"

  res_nld = client.resolve_partner(528)
  assert res_nld["partner_name"] == "Netherlands"


def test_validation_logic():
  """Tests validation report structure and rules."""
  config = {
      "reconciliation_benchmarks_2025": {
          "pitahaya_mag_usd": 272762184.80,
          "pina_mag_usd": 81108645.51,
      }
  }
  validator = TradeValidator(config)

  comtrade_mock = pd.DataFrame([
      {
          "cmd_code": "080430",
          "period": 2025,
          "partner_name": "World",
          "primary_value_usd": 81108645.51,
      },
      {
          "cmd_code": "081090",
          "period": 2025,
          "partner_name": "World",
          "primary_value_usd": 341983617.19,
      },
      {
          "cmd_code": "080450",
          "period": 2025,
          "partner_name": "World",
          "primary_value_usd": 57127810.80,
      },
  ])

  mag_benchmarks = {
      "Piña": {"value_usd": 81108645.51},
      "Pitahaya": {"value_usd": 272762184.80},
  }

  val_df = validator.validate_reconciliation_2025(comtrade_mock, mag_benchmarks)
  assert len(val_df) == 3
  assert (
      val_df.loc[val_df["producto"] == "Piña", "estado_conciliacion"].iloc[0]
      == "CONCILIADO EXACTO"
  )
  assert (
      val_df.loc[val_df["producto"] == "Pitahaya", "estado_conciliacion"].iloc[
          0
      ]
      == "EXPLICADO METODOLÓGICAMENTE"
  )


def test_outputs_exist(base_dir):
  """Tests that all required deliverables (Excel, CSV, Parquet, Charts, Report) exist and are non-empty."""
  outputs_dir = os.path.join(base_dir, "data", "outputs")
  excel_file = os.path.join(outputs_dir, "comercio_frutas_ecuador.xlsx")
  report_file = os.path.join(outputs_dir, "resumen_mercados.md")

  assert os.path.exists(excel_file)
  assert os.path.getsize(excel_file) > 10000

  assert os.path.exists(report_file)
  assert os.path.getsize(report_file) > 1000

  charts_dir = os.path.join(outputs_dir, "charts")
  for i in range(1, 8):
    chart_matches = [
        f for f in os.listdir(charts_dir) if f.startswith(f"{i}_")
    ]
    assert len(chart_matches) == 1
    assert os.path.getsize(os.path.join(charts_dir, chart_matches[0])) > 20000
