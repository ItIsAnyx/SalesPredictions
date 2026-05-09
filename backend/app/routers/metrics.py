from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.db import get_db
from app.auth.service import get_current_user

router = APIRouter()

@router.get("/total-price-changes")
def total_price_changes(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    query = text("""
        WITH current_month AS (
            SELECT COUNT(ph.id) AS total
            FROM price_histories ph
            JOIN products p ON p.id = ph.product_id
            JOIN stores s ON s.id = p.store_id
            WHERE s.user_id = :user_id
              AND DATE_TRUNC('month', ph.changed_at) = DATE_TRUNC('month', NOW())
        ),
        previous_month AS (
            SELECT COUNT(ph.id) AS total
            FROM price_histories ph
            JOIN products p ON p.id = ph.product_id
            JOIN stores s ON s.id = p.store_id
            WHERE s.user_id = :user_id
              AND DATE_TRUNC('month', ph.changed_at) =
                  DATE_TRUNC('month', NOW() - INTERVAL '1 month')
        ),
        total_changes AS (
            SELECT COUNT(ph.id) AS total
            FROM price_histories ph
            JOIN products p ON p.id = ph.product_id
            JOIN stores s ON s.id = p.store_id
            WHERE s.user_id = :user_id
        )
        SELECT
            total_changes.total AS total_value,

            CASE
                WHEN previous_month.total = 0 THEN 100
                ELSE ROUND(
                    (
                        (current_month.total - previous_month.total)::numeric / previous_month.total
                    ) * 100, 2)
            END AS trend
        FROM total_changes, current_month, previous_month
    """)

    result = db.execute(
        query,
        {"user_id": user.id}
    ).mappings().first()

    return {
        "data": {
            "value": result["total_value"] or 0,
            "trend": float(result["trend"]) if result["trend"] else 0
        }
    }

@router.get("/most-changable-product")
def most_changable_product(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    query = text("""
        SELECT
            p.id,
            p.title,
            COUNT(ph.id) AS total_changes
        FROM products p
        JOIN price_histories ph ON ph.product_id = p.id
        JOIN stores s ON s.id = p.store_id
        WHERE s.user_id = :user_id
        GROUP BY p.id, p.title
        ORDER BY total_changes DESC
        LIMIT 1
    """)

    result = db.execute(
        query,
        {"user_id": user.id}
    ).mappings().first()

    return {
        "data": {
            "id": result["id"] if result else 0,
            "title": result["title"] if result else "",
            "value": result["total_changes"] if result else 0
        }
    }

@router.get("/most-active-month")
def most_active_month(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    query = text("""
        SELECT
            TO_CHAR(
                DATE_TRUNC('month', ph.changed_at),
                'YYYY-MM'
            ) AS month,
            COUNT(ph.id) AS changes_count
        FROM price_histories ph
        JOIN products p ON p.id = ph.product_id
        JOIN stores s ON s.id = p.store_id
        WHERE s.user_id = :user_id
        GROUP BY DATE_TRUNC('month', ph.changed_at)
        ORDER BY changes_count DESC
        LIMIT 1
    """)

    result = db.execute(
        query,
        {"user_id": user.id}
    ).mappings().first()

    return {
        "data": {
            "month": result["month"] if result else "",
            "value": result["changes_count"] if result else 0
        }
    }

@router.get("/most-unstable-product")
def most_unstable_product(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    query = text("""
        SELECT
            p.id,
            p.title,
            MAX(ph.price) - MIN(ph.price) AS price_difference
        FROM products p
        JOIN price_histories ph ON ph.product_id = p.id
        JOIN stores s ON s.id = p.store_id
        WHERE s.user_id = :user_id
        GROUP BY p.id, p.title
        ORDER BY price_difference DESC
        LIMIT 1
    """)

    result = db.execute(
        query,
        {"user_id": user.id}
    ).mappings().first()

    return {
        "data": {
            "id": result["id"] if result else 0,
            "title": result["title"] if result else "",
            "value": float(result["price_difference"]) if result else 0
        }
    }

@router.get("/most-active-category")
def most_active_category(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    query = text("""
        SELECT
            c.title,
            COUNT(ph.id) AS total_changes
        FROM categories c
        JOIN products p ON p.category_id = c.id
        JOIN price_histories ph ON ph.product_id = p.id
        JOIN stores s ON s.id = p.store_id
        WHERE s.user_id = :user_id
        GROUP BY c.id, c.title
        ORDER BY total_changes DESC
        LIMIT 1
    """)

    result = db.execute(
        query,
        {"user_id": user.id}
    ).mappings().first()

    return {
        "data": {
            "title": result["title"] if result else "",
            "value": result["total_changes"] if result else 0
        }
    }

@router.get("/avg-price-change-range")
def avg_price_change_range(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    query = text("""
        SELECT ROUND(AVG(diff_days), 2) AS avg_days_between_changes
        FROM (
            SELECT
                EXTRACT(
                    EPOCH FROM (
                        ph.changed_at -
                        LAG(ph.changed_at)
                        OVER (
                            PARTITION BY ph.product_id
                            ORDER BY ph.changed_at
                        )
                    )
                ) / 86400 AS diff_days
            FROM price_histories ph
            JOIN products p ON p.id = ph.product_id
            JOIN stores s ON s.id = p.store_id
            WHERE s.user_id = :user_id
        ) t
        WHERE diff_days IS NOT NULL
    """)

    result = db.execute(
        query,
        {"user_id": user.id}
    ).scalar()

    return {
        "data": {
            "value": float(result) if result else 0
        }
    }