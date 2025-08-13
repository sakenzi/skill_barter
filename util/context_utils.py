from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from model.models import User


async def get_user_by_first_name(first_name: str, db: AsyncSession) -> User:
    user = await db.execute(
        select(User)
        .filter(User.first_name==first_name)
    )  
    return user.scalar_one_or_none()


async def get_user_by_id(user_id: int, db: AsyncSession) -> User:
    user = await db.execute(
        select(User)
        .filter(User.id==user_id)
    )
    return user.scalars().first()