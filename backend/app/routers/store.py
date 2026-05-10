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
    
    try:
        result = db.execute(
            text("""
                SELECT get_products_for_stores_page(
                    :store_id,
                    :region_id,
                    :page,
                    :limit
                )
            """),
            {
                "store_id": store_id,
                "region_id": region_id,
                "page": page,
                "limit": limit
            }
        ).scalar()

        if not result:
            raise HTTPException(500, "EMPTY_RESPONSE")

        if not result.get("success"):
            raise HTTPException(400, result.get("error", "UNKNOWN_ERROR"))
        return result

    except Exception as e:
        raise HTTPException(500, "FAILED_TO_FETCH_STORE_PRODUCTS")

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