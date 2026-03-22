from fastapi import APIRouter

from app.api.v1 import auth, transactions, bills, goals, analytics, ai

router = APIRouter()

router.include_router(auth.router)
router.include_router(transactions.router)
router.include_router(bills.router)
router.include_router(goals.router)
router.include_router(analytics.router)
router.include_router(ai.router)
