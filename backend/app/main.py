import os
from datetime import date, time
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from app.domain.metrics import calculate_metrics
from app.domain.selection import decision_cutoff, select_decision_vintage
from app.services.demo_data import demo_series
from app.domain.models import AccuracyMetrics, ForecastResponse

app = FastAPI(title="Wind Procurement Dashboard API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
TIMEZONE = os.getenv("DECISION_TIMEZONE", "Europe/London")
CUTOFF = time.fromisoformat(os.getenv("DECISION_CUTOFF", "11:00"))


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "data_mode": "demo snapshot", "timezone": TIMEZONE}


@app.get("/api/forecast", response_model=ForecastResponse)
def forecast(delivery_date: date = Query(...)) -> ForecastResponse:
    points, actuals = demo_series(delivery_date)
    cutoff = decision_cutoff(delivery_date, CUTOFF, TIMEZONE)
    return ForecastResponse(delivery_date=delivery_date, decision_cutoff=cutoff, points=select_decision_vintage(points, cutoff), actuals=actuals)


@app.get("/api/accuracy", response_model=AccuracyMetrics)
def accuracy(start_date: date = Query(date(2026, 1, 1)), end_date: date = Query(date(2026, 1, 31))) -> AccuracyMetrics:
    actual, predicted = [], []
    current = start_date
    while current <= end_date:
        forecasts, actuals = demo_series(current)
        actual.extend(x.generation_mw for x in actuals)
        predicted.extend(x.generation_mw for x in forecasts)
        current = date.fromordinal(current.toordinal() + 1)
    return calculate_metrics(actual, predicted)

