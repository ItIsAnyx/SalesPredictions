from fastapi import Response
from app.config import settings
from app.auth.auth_tokens import create_access_token, create_refresh_token
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def create_access_refresh_tokens_to_cookie(
        response: Response, 
        sub: int
    ):
    return set_access_refresh_tokens_to_cookie(
        response,
        create_access_token(sub),
        create_refresh_token(sub)
    )
    

def set_access_refresh_tokens_to_cookie(
        response: Response,
        access_token: str, 
        refresh_token: str
    ):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE
    )

    return response

def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)