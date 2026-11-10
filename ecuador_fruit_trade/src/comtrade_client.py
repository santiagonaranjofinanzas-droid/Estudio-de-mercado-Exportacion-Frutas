"""UN Comtrade API Client for bilateral trade statistics by Harmonized System (HS) code.

Documentation: https://comtradeplus.un.org/en/api-docs
Endpoint: https://comtradeapi.un.org/public/v1/preview/C/A/HS
"""

import os
import json
import time
import requests
import pandas as pd
from typing import Optional, Dict, Any, List
from datetime import datetime


class UNComtradeClient:
    """Client for UN Comtrade Public Preview API with throttling, caching and partner resolution."""

    BASE_URL = "https://comtradeapi.un.org/public/v1/preview/C/A/HS"

    def __init__(
        self,
        raw_storage_dir: str = "ecuador_fruit_trade/data/raw/comtrade",
        partner_areas_file: str = "ecuador_fruit_trade/data/raw/partnerAreas.json",
        subscription_key: Optional[str] = None,
        rate_limit_delay: float = 1.6,
        timeout: int = 25,
    ):
        self.raw_storage_dir = raw_storage_dir
        self.partner_areas_file = partner_areas_file
        self.subscription_key = subscription_key or os.getenv("COMTRADE_API_KEY")
        self.rate_limit_delay = rate_limit_delay
        self.timeout = timeout
        os.makedirs(self.raw_storage_dir, exist_ok=True)

        self.session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) EcuadorFruitTradeAnalysis/1.0",
            "Accept": "application/json",
        }
        if self.subscription_key:
            headers["Ocp-Apim-Subscription-Key"] = self.subscription_key
        self.session.headers.update(headers)

        self._partner_map: Dict[int, Dict[str, Any]] = {}
        self._load_partner_areas()

    def _load_partner_areas(self):
        """Loads reference partner code mapping (id -> Country name, ISO2, ISO3)."""
        if os.path.exists(self.partner_areas_file):
            try:
                with open(self.partner_areas_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                results = data.get("results", [])
                for item in results:
                    pid = item.get("id")
                    if pid is not None:
                        self._partner_map[int(pid)] = {
                            "partner_name": item.get("text", "Unknown"),
                            "partner_iso2": item.get("PartnerCodeIsoAlpha2"),
                            "partner_iso3": item.get("PartnerCodeIsoAlpha3"),
                        }
            except Exception as e:
                print(f"Warning: could not load partnerAreas.json: {e}")

    def resolve_partner(self, partner_code: int) -> Dict[str, Any]:
        """Resolves numerical UN country code to human-readable metadata."""
        if partner_code == 0:
            return {
                "partner_name": "World",
                "partner_iso2": "WLD",
                "partner_iso3": "WLD",
            }
        return self._partner_map.get(
            int(partner_code),
            {
                "partner_name": f"Country_{partner_code}",
                "partner_iso2": None,
                "partner_iso3": None,
            },
        )

    def _request_with_backoff(
        self, params: Dict[str, Any], max_retries: int = 4
    ) -> Optional[Dict[str, Any]]:
        """Executes GET request respecting rate limits and handling 429/5xx status codes."""
        for attempt in range(1, max_retries + 1):
            time.sleep(self.rate_limit_delay)
            try:
                response = self.session.get(
                    self.BASE_URL, params=params, timeout=self.timeout
                )
                if response.status_code == 200:
                    data = response.json()
                    # UN Comtrade preview returns null count when throttled
                    if data.get("count") is None and data.get("data") is None:
                        backoff = attempt * 2.5
                        time.sleep(backoff)
                        continue
                    return data
                elif response.status_code in [429, 500, 502, 503, 504]:
                    backoff = attempt * 3.0
                    time.sleep(backoff)
                else:
                    print(
                        f"UN Comtrade request failed ({response.status_code}): {response.text[:200]}"
                    )
                    return None
            except requests.RequestException as e:
                if attempt == max_retries:
                    print(f"UN Comtrade network error: {e}")
                    return None
                time.sleep(attempt * 2.0)
        return None

    def query(
        self,
        reporter_code: int,
        period: int,
        cmd_code: str,
        flow_code: str = "X",
        partner_code: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Queries trade flow records for a given reporter, year, HS code and flow."""
        params: Dict[str, Any] = {
            "reporterCode": reporter_code,
            "period": period,
            "cmdCode": cmd_code,
            "flowCode": flow_code,
        }
        if partner_code is not None:
            params["partnerCode"] = partner_code

        # Check local cache first
        filename = f"comtrade_{reporter_code}_{period}_{cmd_code}_{flow_code}_{partner_code or 'all'}.json"
        raw_path = os.path.join(self.raw_storage_dir, filename)

        if os.path.exists(raw_path):
            try:
                with open(raw_path, "r", encoding="utf-8") as f:
                    cached_data = json.load(f)
                return cached_data.get("records", [])
            except Exception:
                pass

        data = self._request_with_backoff(params)
        timestamp = datetime.utcnow().isoformat()

        if not data or "data" not in data:
            return []

        raw_records = data.get("data", [])
        count = data.get("count", 0)
        if count == 500:
            print(
                f"WARNING: UN Comtrade query returned exactly 500 records. Possible truncation for params: {params}"
            )

        processed_records = []
        for r in raw_records:
            p_code = r.get("partnerCode")
            p_info = self.resolve_partner(p_code) if p_code is not None else {}

            val_usd = float(r.get("primaryValue") or 0.0)
            net_wgt = (
                float(r.get("netWgt")) if r.get("netWgt") is not None else None
            )
            qty = float(r.get("qty")) if r.get("qty") is not None else None

            # Unit price FOB / CIF calculation
            unit_price_fob_kg = None
            if net_wgt and net_wgt > 0 and val_usd > 0:
                unit_price_fob_kg = val_usd / net_wgt
            elif qty and qty > 0 and val_usd > 0:
                # Sometimes netWgt is missing but qty is in kg (qtyUnitCode 8)
                if r.get("qtyUnitCode") == 8:
                    unit_price_fob_kg = val_usd / qty

            rec = {
                "source": "UN_Comtrade",
                "period": int(r.get("period") or period),
                "reporter_code": int(r.get("reporterCode") or reporter_code),
                "flow_code": r.get("flowCode") or flow_code,
                "cmd_code": str(r.get("cmdCode") or cmd_code),
                "partner_code": int(p_code) if p_code is not None else None,
                "partner_name": p_info.get("partner_name"),
                "partner_iso2": p_info.get("partner_iso2"),
                "partner_iso3": p_info.get("partner_iso3"),
                "primary_value_usd": val_usd,
                "net_weight_kg": net_wgt,
                "qty": qty,
                "qty_unit_code": r.get("qtyUnitCode"),
                "qty_unit_abbr": r.get("qtyUnitAbbr"),
                "fob_value_usd": float(r.get("fobvalue") or 0.0)
                if r.get("fobvalue")
                else None,
                "cif_value_usd": float(r.get("cifvalue") or 0.0)
                if r.get("cifvalue")
                else None,
                "unit_price_usd_kg": unit_price_fob_kg,
                "is_leaf": r.get("isLeaf"),
                "extraction_timestamp": timestamp,
            }
            processed_records.append(rec)

        # Save to raw cache
        with open(raw_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "params": params,
                    "count": count,
                    "extraction_timestamp": timestamp,
                    "records": processed_records,
                },
                f,
                indent=2,
            )

        return processed_records

    def fetch_ecuador_fruit_exports(
        self, cmd_code: str, years: List[int]
    ) -> pd.DataFrame:
        """Fetches Ecuador exports (flowCode='X', reporterCode=218) across a list of years."""
        all_records = []
        for y in years:
            recs = self.query(
                reporter_code=218, period=y, cmd_code=cmd_code, flow_code="X"
            )
            all_records.extend(recs)
        return pd.DataFrame(all_records)

    def fetch_market_imports_and_suppliers(
        self, market_reporter_code: int, cmd_code: str, year: int
    ) -> pd.DataFrame:
        """Fetches imports (flowCode='M') by a target market from all trading partners."""
        recs = self.query(
            reporter_code=market_reporter_code,
            period=year,
            cmd_code=cmd_code,
            flow_code="M",
        )
        return pd.DataFrame(recs)
