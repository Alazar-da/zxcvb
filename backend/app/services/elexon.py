import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import httpx

from app.domain.models import ActualPoint, ForecastPoint


class ElexonClient:
    def __init__(self, base_url: str, cache_dir: Path):
        self.base_url, self.cache_dir = base_url.rstrip("/"), cache_dir
        cache_dir.mkdir(parents=True, exist_ok=True)

    def _get(self, path: str, params: dict[str, str]) -> list[dict]:
        key = self.cache_dir / (path.replace("/", "_") + "_" + params["from"].replace(":", "") + ".json")
        if key.exists():
            return json.loads(key.read_text())
        for attempt in range(3):
            try:
                response = httpx.get(self.base_url + path, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                key.write_text(json.dumps(data))
                return data
            except httpx.HTTPError:
                if attempt == 2:
                    raise
        return []

    def forecast(self, delivery_date: date) -> list[ForecastPoint]:
        start = datetime.combine(delivery_date, datetime.min.time(), timezone.utc)
        rows = self._get("/forecast/generation/wind/history", {"from": start.isoformat(), "to": (start + timedelta(days=1)).isoformat()})
        return [ForecastPoint(start_time=r["startTime"], publish_time=r["publishTime"], generation_mw=r["generation"]) for r in rows]

    def actuals(self, delivery_date: date) -> list[ActualPoint]:
        start = datetime.combine(delivery_date, datetime.min.time(), timezone.utc)
        rows = self._get("/datasets/FUELHH/stream", {"from": start.isoformat(), "to": (start + timedelta(days=1)).isoformat()})
        return [ActualPoint(start_time=r["startTime"], generation_mw=r["generation"]) for r in rows if r.get("fuelType") == "WIND"]

