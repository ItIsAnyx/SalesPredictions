from fastapi import APIRouter, Query, Depends, HTTPException
from app.auth.service import get_admin_current_user
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.db import get_db
from app.schemas.region import RegionPayload

router = APIRouter()

@router.get("")
def get_regions(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, le=100),
    db: Session = Depends(get_db),
    admin = Depends(get_admin_current_user)
):
    offset = (page - 1) * limit

    total_items = db.execute(
        text("""
            SELECT COUNT(id)
            FROM regions
        """)
    ).scalar()

    total_pages = (total_items + limit - 1) // limit if total_items else 1

    regions = db.execute(
        text("""
            SELECT
                id,
                title
            FROM regions
            ORDER BY id ASC
            LIMIT :limit
            OFFSET :offset
        """),
        {
            "limit": limit,
            "offset": offset
        }
    ).mappings().all()

    return {
        "total_items": total_items,
        "total_pages": total_pages,
        "page": page,
        "items": [
            {
                "id": c["id"],
                "title": c["title"]
            }
            for c in regions
        ]
    }

@router.post("")
def create_region(
    payload: RegionPayload,
    db: Session = Depends(get_db),
    admin = Depends(get_admin_current_user)
):
    region_id = db.execute(
        text("""
            INSERT INTO regions(title)
            VALUES (:title)
            RETURNING id
        """),
        {
            "title": payload.title
        }
    ).scalar()

    db.commit()

    return {
        "success": True,
        "data": {
            "id": region_id,
            "title": payload.title
        }
    }


@router.patch("/{region_id}")
def update_region(
    region_id: int,
    payload: RegionPayload,
    db: Session = Depends(get_db),
    admin = Depends(get_admin_current_user)
):
    result = db.execute(
        text("""
            UPDATE regions
            SET title = :title
            WHERE id = :region_id
            RETURNING id
        """),
        {
            "title": payload.title,
            "region_id": region_id
        }
    ).scalar()

    db.commit()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="REGION_NOT_FOUND"
        )

    return {
        "success": True
    }

@router.delete("/{region_id}")
def delete_region(
    region_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_admin_current_user)
):
    result = db.execute(
        text("""
            DELETE FROM regions
            WHERE id = :region_id
            RETURNING id
        """),
        {
            "region_id": region_id
        }
    ).scalar()

    db.commit()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="REGION_NOT_FOUND"
        )

    return {
        "success": True
    }