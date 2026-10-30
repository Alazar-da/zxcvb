from datetime import datetime, date
from pydantic import BaseModel, Field


class ForecastPoint(BaseModel):
    start_time: datetime
    publish_time: datetime
    generation_mw: float


class ActualPoint(BaseModel):
    start_time: datetime
    generation_mw: float


class ForecastResponse(BaseModel):
    delivery_date: date
    decision_cutoff: datetime
    points: list[ForecastPoint]
    actuals: list[ActualPoint] = Field(default_factory=list)


class AccuracyMetrics(BaseModel):
    count: int
    mae_mw: float
    rmse_mw: float
    normalized_error_pct: float
    mean_bias_mw: float
    p90_abs_error_mw: float
    p95_abs_error_mw: float

