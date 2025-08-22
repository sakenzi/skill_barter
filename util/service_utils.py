import hashlib
from datetime import datetime, timedelta
from fastapi import HTTPException, Request
from typing import Optional, Tuple
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from db.database import async_session_factory
from model.models import User
from util.context_utils import get_user_by_first_name, get_user_by_id



def hash_password(plain_password: str) -> str:
    return hashlib.sha256(plain_password.encode("utf-8")).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password


def create_access_token(data: dict, expire_delta: Optional[timedelta] = None) -> Tuple[str, datetime]:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expire_delta or timedelta(minutes=60))
    to_encode.update({'exp': expire, 'sub': str(data.get('sub'))})
    encoded_jwt = jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)
    return encoded_jwt, expire


def get_access_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header is missing")
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    return parts[1]


def validate_token(access_token: str) -> str:
    try:
        payload = jwt.decode(access_token, settings.TOKEN_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=401, detail="Invalid token: 'sub' is missing")
        return int(sub)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")


async def get_user_by_token(access_token: str, db) -> User:
    user_id = await validate_token(access_token)
    user = await get_user_by_id(user_id=int(user_id), db=db)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user