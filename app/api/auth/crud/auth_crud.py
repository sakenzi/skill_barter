from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from model.models import UserEmail, User


async def dal_get_user_email_by_email(email: str, db: AsyncSession) -> UserEmail | None:
    res = await db.execute(select(UserEmail).where(UserEmail.email == email))
    return res.scalar_one_or_none()


async def dal_upsert_verification_code(email: str, code: int, db: AsyncSession) -> UserEmail:
    rec = await dal_get_user_email_by_email(email=email, db=db)
    if rec:
        rec.code = code
        rec.created_at = datetime.utcnow()
        await db.commit()
        await db.refresh(rec)
        return rec
    rec = UserEmail(email=email, code=code)
    db.add(rec)
    await db.commit()
    await db.refresh(rec)
    return rec


async def dal_get_user_email_by_code(code: int, db: AsyncSession) -> UserEmail | None:
    res = await db.execute(select(UserEmail).where(UserEmail.code == code))
    return res.scalar_one_or_none()


async def dal_clear_verification_code(user_email_id: int, db: AsyncSession) -> UserEmail:
    res = await db.execute(select(UserEmail).where(UserEmail.id == user_email_id))
    rec = res.scalar_one_or_none()
    if rec:
        rec.code = None
        await db.commit()
        await db.refresh(rec)
    return rec


async def dal_get_user_by_email(email: str, db: AsyncSession) -> User | None:
    stmt = select(User).join(UserEmail).where(UserEmail.email == email)
    res = await db.execute(stmt)
    return res.scalar_one_or_none()


async def dal_create_user(data: dict, db: AsyncSession) -> User:
    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        surname=data.get("surname") or "",
        phone_number=data["phone_number"],
        password=data["password"],            
        user_email_id=data["user_email_id"]
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def dal_get_user_by_user_email_id(user_email_id: int, db: AsyncSession) -> User | None:
    res = await db.execute(select(User).where(User.user_email_id == user_email_id))
    return res.scalar_one_or_none()