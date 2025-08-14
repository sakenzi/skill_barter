from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.auth.schemas.create import EmailRequest, UserCreate, UserLogin
from app.api.auth.schemas.response import TokenResponse, MessageResponse
from util.context_utils import get_user_by_first_name
from util.service_utils import hash_password
from model.models import UserEmail, User
from sqlalchemy import select


async def dal_create_email_verification(email: str, code: int, db: AsyncSession) -> UserEmail:
    user_email = UserEmail(email=email, code=code)
    db.add(user_email)
    await db.commit()
    await db.refresh(user_email)
    return user_email


async def dal_get_email_by_code(code: int, db: AsyncSession) -> UserEmail | None:
    query = await db.execute(select(UserEmail).where(UserEmail.code==code))
    return query.scalar_one_or_none()


async def dal_mark_email_verified(user_email: UserEmail, db: AsyncSession):
    user_email.code = None
    await db.commit()
    await db.refresh(user_email)
    return user_email


async def dal_create_user(data: dict, db: AsyncSession) -> User:
    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        surname=data["data"],
        phone_number=data["phone_number"],
        password=hash_password(data["password"]),
        user_email_id=data["user_email_id"]
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def dal_get_user_by_email(email: str, db: AsyncSession) -> User | None:
    query = await db.execute(
        select(User)
        .join(UserEmail)
        .where(UserEmail.email==email)
    )
    return query.scalar_one_or_none()