from datetime import date, datetime, timedelta, timezone
from math import sin

from app.domain.models import ActualPoint, ForecastPoint


def demo_series(delivery_date: date) -> tuple[list[ForecastPoint], list[ActualPoint]]:
    base = datetime.combine(delivery_date, datetime.min.time(), timezone.utc)
    forecast, actuals = [], []
    published = base - timedelta(days=1, hours=1)
    for i in range(48):
        start = base + timedelta(minutes=30 * i)
        value = 7200 + 2400 * sin(i / 48 * 6.28 - 1.2)
        forecast.append(ForecastPoint(start_time=start, publish_time=published, generation_mw=round(value)))
        actuals.append(ActualPoint(start_time=start, generation_mw=round(value + 300 * sin(i / 4) + 140)))
    return forecast, actuals

