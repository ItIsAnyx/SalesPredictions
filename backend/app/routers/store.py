from fastapi import APIRouter, Depends, Query, HTTPException

from app.auth.service import get_current_user
from app.schemas.store import StoreItemDto, StoreListDto, StoreCreateDto
from app.database.db import get_db
from app.database.models import Store
from math import ceil
from sqlalchemy import text
from sqlalchemy.orm import Session
from math import ceil

router = APIRouter()

@router.get("", response_model=StoreListDto)
def get_stores(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Store).filter(Store.user_id == user.id)

    total_items = query.count()
    total_pages = ceil(total_items / limit) if total_items else 1

    items = (
        query
        .order_by(Store.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return StoreListDto(
        total_items=total_items,
        page=page,
        total_pages=total_pages,
        items=[
            StoreItemDto.model_validate(item)
            for item in items
        ]
    )

@router.get("/{store_id}/products")
def get_products(
    store_id: int,
    region_id: int | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, le=100),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    store = db.query(Store).filter(
        Store.id == store_id,
        Store.user_id == user.id
    ).first()

    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    offset = (page - 1) * limit

    data_query = text("""
    WITH ranked_prices AS (
        SELECT
            p.id AS product_id,
            p.title,
            ph.region_id,
            ph.price,
            ph.changed_at,
            ROW_NUMBER() OVER (
                PARTITION BY p.id, ph.region_id
                ORDER BY ph.changed_at DESC NULLS LAST
            ) AS rn
        FROM products p
        LEFT JOIN price_histories ph ON ph.product_id = p.id
        WHERE p.store_id = :store_id
        AND (:region_id IS NULL OR ph.region_id = :region_id OR ph.region_id IS NULL)
    ),

    last_two AS (
        SELECT *
        FROM ranked_prices
        WHERE rn <= 2
    ),

    per_region AS (
        SELECT
            product_id,
            region_id,
            title,
            MAX(CASE WHEN rn = 1 THEN price END) AS last_price,
            MAX(CASE WHEN rn = 2 THEN price END) AS prev_price,
            MAX(CASE WHEN rn = 1 THEN changed_at END) AS last_change_time
        FROM last_two
        GROUP BY product_id, region_id, title
    ),

    product_metrics AS (
        SELECT
            product_id,
            title,
            AVG(last_price) AS avg_last_price,
            (AVG(last_price) - AVG(prev_price)) / NULLIF(AVG(prev_price), 0) * 100 AS diff_percent,
            MAX(last_change_time) AS last_change
        FROM per_region
        GROUP BY product_id, title
    )

    SELECT *
    FROM product_metrics
    ORDER BY last_change DESC
    LIMIT :limit OFFSET :offset
    """)

    items = db.execute(data_query, {
        "store_id": store_id,
        "region_id": region_id,
        "limit": limit,
        "offset": offset
    }).mappings().all()

    count_query = text("""
        WITH prices AS (
            SELECT
                p.id AS product_id
            FROM products p
            LEFT JOIN price_histories ph ON ph.product_id = p.id
            WHERE (:region_id IS NULL OR ph.region_id = :region_id)
                AND p.store_id = :store_id
        )
        SELECT COUNT(DISTINCT product_id)
        FROM prices
        """)

    total_items = db.execute(count_query, {
        "store_id": store_id,
        "region_id": region_id
    }).scalar()

    total_pages = ceil(total_items / limit) if total_items else 1

    return {
        "total_items": total_items,
        "page": page,
        "total_pages": total_pages,
        "items": items
    }

@router.post("")
def create_store(
    body: StoreCreateDto,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    store = Store(
        title=body.store_name,
        user_id=user.id
    )

    db.add(store)
    db.commit()

    return {"status": "ok"}