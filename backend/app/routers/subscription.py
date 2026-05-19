from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text

from app.database.db import get_db
from app.database.models import PurchaseHistory, Subscription
from app.database.models import User
from app.auth.service import get_current_user
from app.schemas.subscription import SubscriptionCreateDto
from sqlalchemy.exc import DataError

router = APIRouter()

def get_active_subscription(
        user_id: int,
        db: Session
) -> PurchaseHistory | None:
    
    now = datetime.now(timezone.utc)

    subscription = (
        db.query(PurchaseHistory)
        .options(joinedload(PurchaseHistory.sub))
        .filter(
            PurchaseHistory.user_id == user_id,
            PurchaseHistory.status == "active",
            PurchaseHistory.start_date <= now,
            PurchaseHistory.end_date >= now
        )
        .first()
    )
    return subscription

def check_subscription_required(
        user_id: int,
        predict_days: int,
        db: Session
):
    if predict_days <= 1:
        return

    subscription = get_active_subscription(user_id, db)

    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="Active subscription required"
        )

@router.get("/me")
def get_my_subscription(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    subscription = get_active_subscription(current_user.id, db)

    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="No active subscription"
        )

    return {
        "subscription_id": subscription.id,
        "subscription_name": subscription.sub.name,
        "status": subscription.status,
        "start_date": subscription.start_date,
        "end_date": subscription.end_date,
        "total_price": float(subscription.total_price)
    }

@router.post("/buy")
def create_subscription(
        body: SubscriptionCreateDto,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    try:
        result = db.execute(
            text("""
                SELECT create_user_subscription(
                    :user_id,
                    :subscription_id,
                    :duration_months
                )
            """),
            {
                "user_id": current_user.id,
                "subscription_id": body.id,
                "duration_months": body.duration_months
            }
        )

        db.commit()

        data = result.scalar()

        return data
    except DataError as e:
        db.rollback()

        error_message = str(e.orig)

        if "Subscription not found" in error_message:
            raise HTTPException(
                status_code=404,
                detail="Subscription not found"
            )

        if "User already has active subscription" in error_message:
            raise HTTPException(
                status_code=400,
                detail="User already has active subscription"
            )

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {error_message}"
        )

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

@router.post("/cancel")
def cancel_subscription(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    subscription = get_active_subscription(current_user.id, db)

    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="No active subscription"
        )

    subscription.status = "cancelled"

    db.commit()

    return {
        "message": "Subscription cancelled"
    }