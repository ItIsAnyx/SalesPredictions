from fastapi import APIRouter, Depends, HTTPException, Query
from app.auth.service import get_admin_current_user
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.db import get_db
from app.schemas.user import ChangeUserRolePayload

router = APIRouter()

@router.get("")
def get_users(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, le=100),
    db: Session = Depends(get_db),
    admin = Depends(get_admin_current_user)
):
    offset = (page - 1) * limit

    total_users = db.execute(
        text("""
            SELECT COUNT(id)
            FROM users
        """)
    ).scalar()

    total_pages = (total_users + limit - 1) // limit

    users = db.execute(
        text("""
            SELECT
                id,
                email,
                login,
                role
            FROM users
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
        "total_items": total_users,
        "total_pages": total_pages,
        "page": page,
        "items": [
            {
                "id": user["id"],
                "email": user["email"],
                "login": user["login"],
                "role": user["role"]
            }
            for user in users
        ]
    }

@router.patch("/{user_id}/role")
def change_user_role(
    user_id: int,
    payload: ChangeUserRolePayload,
    db: Session = Depends(get_db),
    admin = Depends(get_admin_current_user)
):
    if (user_id == admin.id):
        raise HTTPException(400, detail="Can't change your role")
    
    allowed_roles = ["USER", "ADMIN"]

    if (payload.role not in allowed_roles):
        raise HTTPException(400, detail="Not Allowed Role")

    if payload.role not in allowed_roles:
        raise HTTPException(
            status_code=400,
            detail="INVALID_ROLE"
        )

    result = db.execute(
        text("""
            UPDATE users
            SET role = :role
            WHERE id = :user_id
            RETURNING id, role
        """),
        {
            "user_id": user_id,
            "role": payload.role
        }
    ).mappings().first()

    db.commit()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="USER_NOT_FOUND"
        )

    return {
        "success": True,
        "data": {
            "id": result["id"],
            "role": result["role"]
        }
    }

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_admin_current_user)
):
    if (user_id == admin.id):
        raise HTTPException(400, detail="Can't delete your profile")
    
    result = db.execute(
        text("""
            DELETE FROM users
            WHERE id = :user_id
            RETURNING id
        """),
        {
            "user_id": user_id
        }
    ).scalar()

    db.commit()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="USER_NOT_FOUND"
        )

    return {
        "success": True
    }