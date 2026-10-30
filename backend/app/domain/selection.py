from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from .models import ForecastPoint


def decision_cutoff(delivery_date: date, cutoff: time, timezone: str) -> datetime:
    return datetime.combine(delivery_date, cutoff, ZoneInfo(timezone)).astimezone(ZoneInfo("UTC"))


def select_decision_vintage(points: list[ForecastPoint], cutoff: datetime) -> list[ForecastPoint]:
    """Select the newest eligible forecast for every target start time."""
    selected: dict[datetime, ForecastPoint] = {}
    for point in points:
        if point.publish_time <= cutoff and (
            point.start_time not in selected
            or point.publish_time > selected[point.start_time].publish_time
        ):
            selected[point.start_time] = point
    return [selected[key] for key in sorted(selected)]

