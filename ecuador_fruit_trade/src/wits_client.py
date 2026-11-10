"""Client for World Integrated Trade Solution (WITS) SDMX REST API.

Documentation: https://wits.worldbank.org/witsapiintro.aspx?lang=en
Endpoint format: https://wits.worldbank.org/API/V1/SDMX/V21/datasource/<datasource>/reporter/<reporter>/year/<year>/partner/<partner>/product/<product>/indicator/<indicator>
"""

import os
import time
import requests
import xml.etree.ElementTree as ET
import pandas as pd
from typing import Optional, Dict, Any, List
from datetime import datetime


class WITSClient:
    """Robust client for querying World Bank WITS SDMX V2.1 API."""

    BASE_URL = "https://wits.worldbank.org/API/V1/SDMX/V21"

    def __init__(
        self,
        raw_storage_dir: str = "ecuador_fruit_trade/data/raw/wits",
        timeout: int = 20,
        rate_limit_delay: float = 1.0,
    ):
        self.raw_storage_dir = raw_storage_dir
        self.timeout = timeout
        self.rate_limit_delay = rate_limit_delay
        os.makedirs(self.raw_storage_dir, exist_ok=True)

        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) EcuadorFruitTradeResearch/1.0",
                "Accept": "application/xml, text/xml, */*",
            }
        )

    def _request_with_retry(
        self, url: str, max_retries: int = 3
    ) -> Optional[requests.Response]:
        """Executes GET request with exponential backoff on errors."""
        for attempt in range(1, max_retries + 1):
            try:
                time.sleep(self.rate_limit_delay)
                response = self.session.get(url, timeout=self.timeout)
                if response.status_code == 200:
                    return response
                elif response.status_code in [429, 500, 502, 503, 504]:
                    sleep_time = attempt * 2.0
                    time.sleep(sleep_time)
                else:
                    return response
            except requests.RequestException:
                if attempt == max_retries:
                    raise
                time.sleep(attempt * 2.0)
        return None

    def fetch_indicator(
        self,
        datasource: str,
        reporter: str,
        year: int,
        partner: str,
        product: str,
        indicator: str,
    ) -> List[Dict[str, Any]]:
        """Queries a single indicator time series from WITS.

        Example datasource: 'tradestats-trade' or 'tradestats-tariff'
        """
        endpoint = (
            f"{self.BASE_URL}/datasource/{datasource}/reporter/{reporter.lower()}/"
            f"year/{year}/partner/{partner.lower()}/product/{product}/indicator/{indicator}"
        )

        response = self._request_with_retry(endpoint)
        timestamp = datetime.utcnow().isoformat()

        if response is None or response.status_code != 200:
            return []

        # Save raw XML response
        filename = (
            f"wits_{datasource}_{reporter}_{year}_{partner}_{product}_{indicator}.xml"
        )
        safe_filename = "".join(
            c if c.isalnum() or c in "._-" else "_" for c in filename
        )
        raw_path = os.path.join(self.raw_storage_dir, safe_filename)
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(response.text)

        # Parse SDMX XML
        records = []
        try:
            root = ET.fromstring(response.content)
            for series in root.iter():
                if series.tag.endswith("Series"):
                    series_attribs = series.attrib
                    for obs in series.iter():
                        if obs.tag.endswith("Obs"):
                            obs_attribs = obs.attrib
                            records.append(
                                {
                                    "source": "WITS_WorldBank",
                                    "datasource": datasource,
                                    "reporter": series_attribs.get(
                                        "REPORTER", reporter
                                    ),
                                    "partner": series_attribs.get("PARTNER", partner),
                                    "product": series_attribs.get(
                                        "PRODUCTCODE", product
                                    ),
                                    "indicator": series_attribs.get(
                                        "INDICATOR", indicator
                                    ),
                                    "year": int(obs_attribs.get("TIME_PERIOD", year)),
                                    "obs_value": float(
                                        obs_attribs.get("OBS_VALUE", 0.0)
                                    ),
                                    "extraction_timestamp": timestamp,
                                    "endpoint": endpoint,
                                }
                            )
        except ET.ParseError:
            pass

        return records

    def fetch_vegetable_trade_macro(
        self, start_year: int = 2015, end_year: int = 2021
    ) -> pd.DataFrame:
        """Fetches macro sector trade values for Ecuador (06-15_Vegetable).

        Note: WITS tradestats-trade typically has series up to 2021/2022.
        """
        all_records = []
        for year in range(start_year, end_year + 1):
            # Export
            exp_records = self.fetch_indicator(
                datasource="tradestats-trade",
                reporter="ecu",
                year=year,
                partner="wld",
                product="06-15_Vegetable",
                indicator="XPRT-TRD-VL",
            )
            all_records.extend(exp_records)

            # Import
            imp_records = self.fetch_indicator(
                datasource="tradestats-trade",
                reporter="ecu",
                year=year,
                partner="wld",
                product="06-15_Vegetable",
                indicator="MPRT-TRD-VL",
            )
            all_records.extend(imp_records)

        return pd.DataFrame(all_records)

    def fetch_tariff_comparison(
        self,
        destinations: List[str],
        year: int = 2021,
        product: str = "06-15_Vegetable",
    ) -> pd.DataFrame:
        """Fetches effectively applied tariff (AHS) and MFN tariff for Ecuador in target destinations."""
        tariff_records = []
        for dest in destinations:
            for ind in ["AHS-WGHTD-AVRG", "MFN-WGHTD-AVRG"]:
                records = self.fetch_indicator(
                    datasource="tradestats-tariff",
                    reporter=dest,
                    year=year,
                    partner="ecu",
                    product=product,
                    indicator=ind,
                )
                tariff_records.extend(records)

        return pd.DataFrame(tariff_records)
