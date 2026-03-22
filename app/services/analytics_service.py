from datetime import datetime

from app.utils.dates import start_of_month, end_of_month, days_elapsed_this_month, days_remaining_this_month


async def get_monthly_summary(db, user_id: str) -> dict:
    now = datetime.utcnow()
    month_start = start_of_month(now)
    month_end = end_of_month(now)

    pipeline_month = [
        {"$match": {"user_id": user_id, "date": {"$gte": month_start, "$lte": month_end}}},
        {"$group": {"_id": "$type", "total": {"$sum": "$amount"}}},
    ]
    month_results = await db["transactions"].aggregate(pipeline_month).to_list(length=10)
    monthly = {r["_id"]: r["total"] for r in month_results}

    # Balance = all-time income - all-time expense
    pipeline_all = [
        {"$match": {"user_id": user_id}},
        {"$group": {"_id": "$type", "total": {"$sum": "$amount"}}},
    ]
    all_results = await db["transactions"].aggregate(pipeline_all).to_list(length=10)
    all_time = {r["_id"]: r["total"] for r in all_results}

    current_month_income = monthly.get("income", 0.0)
    current_month_expense = monthly.get("expense", 0.0)
    balance = all_time.get("income", 0.0) - all_time.get("expense", 0.0)

    return {
        "current_month_income": current_month_income,
        "current_month_expense": current_month_expense,
        "balance": balance,
    }


async def get_category_breakdown(db, user_id: str) -> dict:
    now = datetime.utcnow()
    month_start = start_of_month(now)
    month_end = end_of_month(now)

    pipeline = [
        {
            "$match": {
                "user_id": user_id,
                "type": "expense",
                "date": {"$gte": month_start, "$lte": month_end},
            }
        },
        {"$group": {"_id": "$category", "amount": {"$sum": "$amount"}}},
        {"$sort": {"amount": -1}},
    ]
    results = await db["transactions"].aggregate(pipeline).to_list(length=100)
    total_expense = sum(r["amount"] for r in results)

    categories = []
    for r in results:
        percentage = round((r["amount"] / total_expense) * 100, 2) if total_expense > 0 else 0.0
        categories.append(
            {"category": r["_id"] or "Uncategorized", "amount": r["amount"], "percentage": percentage}
        )

    return {"categories": categories, "total_expense": total_expense}


async def get_budget_status(db, user_id: str) -> dict:
    summary = await get_monthly_summary(db, user_id)
    current_spending = summary["current_month_expense"]
    current_income = summary["current_month_income"]

    days_elapsed = days_elapsed_this_month()
    days_remaining = days_remaining_this_month()

    if days_elapsed == 0:
        average_daily_spending = 0.0
    else:
        average_daily_spending = current_spending / days_elapsed

    predicted_month_end_spending = current_spending + (average_daily_spending * days_remaining)

    if current_income == 0:
        budget_status = "No Income Data"
        risk_level = "Unknown"
    else:
        ratio = predicted_month_end_spending / current_income
        if ratio < 0.80:
            budget_status = "On Track"
        elif ratio <= 1.0:
            budget_status = "Warning"
        else:
            budget_status = "Over Budget"

        if ratio < 0.60:
            risk_level = "Low"
        elif ratio <= 0.90:
            risk_level = "Medium"
        else:
            risk_level = "High"

    return {
        "budget_status": budget_status,
        "risk_level": risk_level,
        "predicted_month_end_spending": round(predicted_month_end_spending, 2),
        "current_spending": current_spending,
        "current_income": current_income,
        "days_elapsed": days_elapsed,
        "days_remaining": days_remaining,
        "average_daily_spending": round(average_daily_spending, 2),
    }
