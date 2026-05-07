from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.auth.service import get_current_user
from app.database.db import get_db
from sqlalchemy.orm import Session
from app.database.models import Product, PriceHistory, Store
from app.schemas.product import ProductPriceUpdateDto, ProductCreateDto, ProductInfoDto
from sqlalchemy import text
from math import ceil
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/{product_id}/price")
def update_price(
    product_id: int,
    body: ProductPriceUpdateDto,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    product = (
        db.query(Product)
        .join(Store)
        .filter(
            Product.id == product_id,
            Store.user_id == user.id
        )
        .first()
    )

    if not product:
        raise HTTPException(403, "Can't update product or product not found")

    history = PriceHistory(
        product_id=product_id,
        price=body.price,
        region_id=body.region_id,
        season=body.season,
        weather_condition=body.weather_condition,
        weekend=body.weekend
    )

    db.add(history)
    db.commit()

    return {"status": "ok"}

@router.post("")
def create_product(
    body: ProductCreateDto,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    store = db.query(Store).filter(
        Store.id == body.store_id,
        Store.user_id == user.id
    ).first()

    if not store:
        raise HTTPException(403, "Can't add product to this store")

    product = Product(
        title=body.title,
        store_id=body.store_id,
        category_id=body.category_id
    )

    db.add(product)
    db.flush()

    
    if body.price is not None:
        if not all([body.region_id, body.season, body.weather_condition]):
            raise HTTPException(400, "Missing price metadata")
        
        history = PriceHistory(
            product_id=product.id,
            price=body.price,
            region_id=body.region_id,
            season=body.season,
            weather_condition=body.weather_condition,
            weekend=body.weekend
        )
        db.add(history)

    db.commit()
    return product

@router.get("")
def get_products(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, le=100),
    region_id: int | None = Query(default=None),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit

    data_query = text("""
    WITH ranked_prices AS (
        SELECT
            p.id AS product_id,
            p.title,
            s.title as store_title,
            ph.region_id,
            ph.price,
            ROW_NUMBER() OVER (
                PARTITION BY p.id, ph.region_id
                ORDER BY ph.changed_at DESC NULLS LAST
            ) AS rn
        FROM products p
        LEFT JOIN price_histories ph ON ph.product_id = p.id
        LEFT JOIN stores s ON p.store_id = s.id
        WHERE :region_id IS NULL OR ph.region_id = :region_id OR ph.region_id IS NULL
    ),

    last_two AS (
        SELECT *
        FROM ranked_prices
        WHERE rn <= 2
    ),

    per_region AS (
        SELECT
            product_id,
            title,
            store_title,
            MAX(CASE WHEN rn = 1 THEN price END) AS last_price,
            MAX(CASE WHEN rn = 2 THEN price END) AS prev_price
        FROM last_two
        GROUP BY product_id, title, store_title
    ),

    product_metrics AS (
        SELECT
            product_id,
            title,
            store_title,
            AVG(last_price) AS avg_last_price,
            (AVG(last_price) - AVG(prev_price)) / NULLIF(AVG(prev_price), 0) * 100 AS diff_percent
        FROM per_region
        GROUP BY product_id, title, store_title
    )

    SELECT *
    FROM product_metrics
    LIMIT :limit OFFSET :offset
    """)

    items = db.execute(data_query, {
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
        WHERE :region_id IS NULL OR ph.region_id = :region_id
    )
    SELECT COUNT(DISTINCT product_id)
    FROM prices
    """)

    total_items = db.execute(count_query, {
        "region_id": region_id
    }).scalar()

    total_pages = ceil(total_items / limit) if total_items else 1

    return {
        "total_items": total_items,
        "page": page,
        "total_pages": total_pages,
        "items": items
    }

@router.get("/growth")
def get_products_growth(
    db: Session = Depends(get_db),
    region_id: int | None = Query(default=None)
):
    seven_days_ago = datetime.utcnow() - timedelta(days=7)

    query = db.query(Product).filter(
        Product.created_at >= seven_days_ago
    )

    if region_id is not None:
        query = query.join(PriceHistory).filter(
            PriceHistory.region_id == region_id
        )

    count = query.distinct(Product.id).count()

    return {"growth": count}

@router.get("/{product_id}", response_model=ProductInfoDto)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).where(Product.id == product_id).first()

    return ProductInfoDto(
        id=product.id,
        title=product.title
    )

@router.get("/{product_id}/prices")
def get_prices(product_id: int, 
               range: int = Query(default=10000), 
               db: Session = Depends(get_db)
               ):
    return

@router.get("/{product_id}/prices-prediction")
def get_prices(product_id: int, 
               range: int = Query(default=10000),
               db: Session = Depends(get_db)
               ):
    return