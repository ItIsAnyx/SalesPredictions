from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.models import PriceHistory, Region, Category, User

router = APIRouter()

@router.get("/meta/price-history-options")
def get_price_options(db: Session = Depends(get_db)):
    return get_weather_region(db)

@router.get("/meta/create-product-options")
def get_product_options(db: Session = Depends(get_db)):
    categories = db.query(Category).all()

    body = get_weather_region(db)
    body["categories"] = categories
    
    return body

@router.get("/meta/regions")
def get_regions(db: Session = Depends(get_db)):
    return {
        "regions": db.query(Region).all()
    }

@router.get("/meta/roles")
def get_regions():
    return {
        "roles": User.__table__.columns["role"].type.enums
    }

def get_weather_region(db: Session):
    regions = db.query(Region).all()

    return {
        "weather_conditions": PriceHistory.__table__.columns["weather_condition"].type.enums,
        "regions": regions
    }