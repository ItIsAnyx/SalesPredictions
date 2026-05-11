from fastapi import APIRouter, Depends, HTTPException, Query
from app.auth.service import get_admin_current_user
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.db import get_db
from app.schemas.category import CategoryPayload

router = APIRouter()

@router.get("")
def get_categories(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, le=100),
    db: Session = Depends(get_db),
    admin = Depends(get_admin_current_user)
):
    offset = (page - 1) * limit

    total_items = db.execute(
        text("""
            SELECT COUNT(id)
            FROM categories
        """)
    ).scalar()

    total_pages = (total_items + limit - 1) // limit if total_items else 1

    categories = db.execute(
        text("""
            SELECT
                id,
                title
            FROM categories
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
            for c in categories
        ]
    }

@router.post("")
def create_category(
    payload: CategoryPayload,
    db: Session = Depends(get_db),
    admin = Depends(get_admin_current_user)
):
    category_id = db.execute(
        text("""
            INSERT INTO categories(title)
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
            "id": category_id,
            "title": payload.title
        }
    }

@router.patch("/{category_id}")
def update_category(
    category_id: int,
    payload: CategoryPayload,
    db: Session = Depends(get_db),
    admin = Depends(get_admin_current_user)
):
    result = db.execute(
        text("""
            UPDATE categories
            SET title = :title
            WHERE id = :category_id
            RETURNING id
        """),
        {
            "title": payload.title,
            "category_id": category_id
        }
    ).scalar()

    db.commit()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="CATEGORY_NOT_FOUND"
        )

    return {
        "success": True
    }


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_admin_current_user)
):
    try:
        result = db.execute(
            text("""
                DELETE FROM categories
                WHERE id = :category_id
                RETURNING id
            """),
            {
                "category_id": category_id
            }
        ).scalar()
        
        db.commit()

        if not result:
            raise HTTPException(
                status_code=404,
                detail="CATEGORY_NOT_FOUND"
            )

        return {
            "success": True
        }
    except Exception as e:
        print("ERROR:", str(e))