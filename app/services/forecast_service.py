import calendar
import logging
from datetime import datetime
from typing import List, Optional

from app.utils.dates import start_of_month

logger = logging.getLogger(__name__)


async def get_forecast(db, user_id: str) -> dict:
    now = datetime.utcnow()
    month_start = start_of_month(now)
    today_day = now.day
    total_days = calendar.monthrange(now.year, now.month)[1]

    # Fetch current month expense transactions
    docs = await db["transactions"].find(
        {
            "user_id": user_id,
            "type": "expense",
            "date": {"$gte": month_start, "$lte": now},
        }
    ).to_list(length=10000)

    # Build daily totals
    daily_totals: dict = {day: 0.0 for day in range(1, today_day + 1)}
    for doc in docs:
        doc_date = doc.get("date")
        if isinstance(doc_date, datetime):
            day = doc_date.day
            if 1 <= day <= today_day:
                daily_totals[day] = daily_totals.get(day, 0.0) + doc.get("amount", 0.0)

    labels = [
        f"{now.year}-{str(now.month).zfill(2)}-{str(d).zfill(2)}" for d in range(1, total_days + 1)
    ]

    actual: List[Optional[float]] = []
    for d in range(1, total_days + 1):
        if d <= today_day:
            actual.append(daily_totals.get(d, 0.0))
        else:
            actual.append(None)

    # Check if enough data for ARIMA
    actual_values = [v for v in actual if v is not None]
    if len(actual_values) < 3:
        forecast: List[Optional[float]] = [None] * total_days
        return {
            "labels": labels,
            "actual": actual,
            "forecast": forecast,
            "message": "Not enough data for forecast",
        }

    # ARIMA forecast
    try:
        import numpy as np
        from statsmodels.tsa.arima.model import ARIMA

        series = np.array(actual_values, dtype=float)
        remaining_days = total_days - today_day

        forecast_values: List[Optional[float]] = []
        if remaining_days > 0:
            try:
                model = ARIMA(series, order=(5, 1, 0))
                fit = model.fit()
                predictions = fit.forecast(steps=remaining_days)
                forecast_values = [max(0.0, round(float(v), 2)) for v in predictions]
            except Exception:
                try:
                    model = ARIMA(series, order=(1, 0, 0))
                    fit = model.fit()
                    predictions = fit.forecast(steps=remaining_days)
                    forecast_values = [max(0.0, round(float(v), 2)) for v in predictions]
                except Exception as e:
                    logger.warning(f"ARIMA fallback also failed: {e}")
                    avg = float(np.mean(series)) if len(series) > 0 else 0.0
                    forecast_values = [round(avg, 2)] * remaining_days

        forecast = [None] * today_day + forecast_values

    except ImportError:
        logger.warning("statsmodels not installed, skipping ARIMA")
        forecast = [None] * total_days

    return {"labels": labels, "actual": actual, "forecast": forecast}
