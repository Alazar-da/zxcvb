from math import sqrt
from statistics import mean

from .models import AccuracyMetrics


def calculate_metrics(actual: list[float], forecast: list[float]) -> AccuracyMetrics:
    if len(actual) != len(forecast) or not actual:
        raise ValueError("actual and forecast must be equally sized and non-empty")
    errors = [a - f for a, f in zip(actual, forecast)]
    absolute = sorted(abs(e) for e in errors)
    avg_actual = mean(actual)
    def percentile(values: list[float], p: float) -> float:
        index = (len(values) - 1) * p
        lower, upper = int(index), min(int(index) + 1, len(values) - 1)
        return values[lower] + (values[upper] - values[lower]) * (index - lower)
    return AccuracyMetrics(
        count=len(errors),
        mae_mw=mean(absolute),
        rmse_mw=sqrt(mean(e * e for e in errors)),
        normalized_error_pct=(mean(absolute) / avg_actual * 100) if avg_actual else 0,
        mean_bias_mw=mean(errors),
        p90_abs_error_mw=percentile(absolute, .9),
        p95_abs_error_mw=percentile(absolute, .95),
    )

