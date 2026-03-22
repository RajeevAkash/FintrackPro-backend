import json
import logging
from datetime import datetime

from app.services.analytics_service import get_monthly_summary, get_category_breakdown

logger = logging.getLogger(__name__)

FALLBACK_TIPS = [
    {
        "title": "Track Every Expense",
        "description": "Record all your daily expenses to identify where your money is going and find opportunities to save.",
        "priority": "high",
    },
    {
        "title": "Follow the 50/30/20 Rule",
        "description": "Allocate 50% of income to needs, 30% to wants, and 20% to savings and debt repayment.",
        "priority": "high",
    },
    {
        "title": "Build an Emergency Fund",
        "description": "Aim to save at least 3-6 months of living expenses in an easily accessible account.",
        "priority": "high",
    },
    {
        "title": "Review Subscriptions",
        "description": "Audit all recurring subscriptions and cancel ones you no longer use actively.",
        "priority": "medium",
    },
    {
        "title": "Meal Prep to Save on Food",
        "description": "Preparing meals at home instead of dining out can save a significant amount each month.",
        "priority": "medium",
    },
    {
        "title": "Automate Savings",
        "description": "Set up automatic transfers to a savings account on payday so you save before you spend.",
        "priority": "low",
    },
    {
        "title": "Compare Before You Buy",
        "description": "Always compare prices and look for coupons or cashback offers before making a purchase.",
        "priority": "low",
    },
]


async def generate_tips(db, user_id: str) -> dict:
    summary = await get_monthly_summary(db, user_id)
    categories_data = await get_category_breakdown(db, user_id)
    goals = await db["goals"].find({"user_id": user_id}).to_list(length=100)

    income = summary["current_month_income"]
    expense = summary["current_month_expense"]
    balance = summary["balance"]

    category_lines = "\n".join(
        f"  - {c['category']}: {c['amount']} ({c['percentage']}%)"
        for c in categories_data["categories"]
    )
    goals_lines = "\n".join(
        f"  - {g['name']}: target {g['target_amount']}, current {g.get('current_amount', 0)}"
        for g in goals
    ) or "  No goals set."

    prompt = (
        "You are a personal financial advisor. Based on the following financial data, "
        "provide 5-7 specific, actionable savings tips.\n\n"
        f"Monthly Income: {income}\n"
        f"Monthly Expense: {expense}\n"
        f"Balance: {balance}\n\n"
        f"Expense Breakdown:\n{category_lines}\n\n"
        f"Financial Goals:\n{goals_lines}\n\n"
        'Provide tips in JSON format as an array of objects with "title", "description", '
        'and "priority" (high/medium/low) fields.\n'
        "Return ONLY the JSON array, no other text."
    )

    tips = await _call_gemini(prompt)
    return {"tips": tips, "generated_at": datetime.utcnow().isoformat()}


async def _call_gemini(prompt: str) -> list:
    from app.core.config import settings

    if not settings.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY not set, returning fallback tips.")
        return FALLBACK_TIPS

    try:
        import google.generativeai as genai

        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Strip markdown code fences if present
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:-1]) if lines[-1] == "```" else "\n".join(lines[1:])

        tips = json.loads(text)
        if isinstance(tips, list):
            return tips
        return FALLBACK_TIPS
    except Exception as e:
        logger.error("Gemini API call failed: %s", e)
        return FALLBACK_TIPS
