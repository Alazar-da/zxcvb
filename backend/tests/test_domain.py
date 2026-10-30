from datetime import datetime, timezone

from app.domain.metrics import calculate_metrics
from app.domain.models import ForecastPoint
from app.domain.selection import select_decision_vintage


def test_selects_latest_publish_before_cutoff():
    target = datetime(2026, 1, 1, 12, tzinfo=timezone.utc)
    cutoff = datetime(2025, 12, 31, 11, tzinfo=timezone.utc)
    points = [ForecastPoint(start_time=target, publish_time=datetime(2025, 12, 31, 10, tzinfo=timezone.utc), generation_mw=1), ForecastPoint(start_time=target, publish_time=datetime(2025, 12, 31, 12, tzinfo=timezone.utc), generation_mw=2)]
    assert select_decision_vintage(points, cutoff)[0].generation_mw == 1


def test_metrics():
    metrics = calculate_metrics([10, 20], [8, 25])
    assert metrics.mae_mw == 3.5
    assert metrics.mean_bias_mw == 1.5

