from fastapi import APIRouter, Depends, HTTPException, Query
from app.auth.service import get_current_user
from app.database.db import get_db
from sqlalchemy.orm import Session
from app.database.models import Product, PriceHistory, Store
from app.schemas.product import ProductPriceUpdateDto, ProductCreateDto, ProductInfoDto
from sqlalchemy import text
from datetime import datetime, timedelta
import pandas as pd
from app.ml_models.ml_models import train_predict_model

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
    try:
        result = db.execute(
            text("""
                SELECT get_product_for_products_page(
                    :page,
                    :limit,
                    :region_id
                )
            """),
            {
                "page": page,
                "limit": limit,
                "region_id": region_id
            }
        ).scalar()

        if not result:
            raise HTTPException(500, "EMPTY_RESPONSE")

        if not result["success"]:
            raise HTTPException(400, result.get("error", "UNKNOWN_ERROR"))
        return result
    
    except HTTPException:
        raise

    except Exception as e:
         raise HTTPException(500, "FAILED_TO_FETCH_STORE_PRODUCTS")

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
def get_prices(
    product_id: int,
    region_id: int = Query(default=1),
    range_ms: int = Query(default=1_000_000_000),
    db: Session = Depends(get_db)
):
    try:

        result = db.execute(
            text("""
                SELECT get_product_prices(
                    :product_id,
                    :region_id,
                    :range_ms
                )
            """),
            {
                "product_id": product_id,
                "region_id": region_id,
                "range_ms": range_ms
            }
        ).scalar()

        if not result:
            raise HTTPException(500, "EMPTY_RESPONSE")

        if not result["success"]:
            raise HTTPException(400, result.get("error", "UNKNOWN_ERROR"))
        
        return result

    except HTTPException:
        raise

    except Exception as e:
                 raise HTTPException(500, "FAILED_TO_FETCH_STORE_PRODUCTS")


def get_price_history_for_model(product_id: int,
                                region_id: int = 1,
                                range: int = Query(default=1_000_000_000_000),
                                db: Session = Depends(get_db)
                                ):
    today = datetime.utcnow()
    range_day = today - timedelta(milliseconds=range)

    data_query = text("""
    SELECT changed_at, price, season, weather_condition, weekend FROM price_histories
    WHERE product_id = :product_id AND changed_at >= :range_day AND region_id = :region_id
    ORDER BY changed_at ASC
    """)
    price_history = db.execute(data_query, {"product_id": product_id, "range_day": range_day, "region_id": region_id}).mappings().all()
    df = pd.DataFrame(price_history)
    print("get_price_history_for_model")
    print(df.head())
    print(df.tail())

    return df

@router.get("/{product_id}/price-prediction")
def get_prices(product_id: int,
               region_id: int = 1,
               range: int = Query(default=1_000_000_000_000),
               predict_days: int = Query(default=7),
               db: Session = Depends(get_db)
               ):
    try:
        df = get_price_history_for_model(product_id, region_id, range, db)
        result = train_predict_model(df, range_days=predict_days, is_debugging=False)
        return [
            {
                "timestamp": date.isoformat(),
                "price": float(price)
            }
            for date, price in zip(result["timestamp"], result["predictions"])
        ]

    except Exception as e:
        print("ERROR ", str(e))
        raise HTTPException(status_code=400, detail=f"Error when trying to predict prices: {str(e)}")