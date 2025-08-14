from datetime import datetime, timedelta
import re
from model.models import UserEmail
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.auth.schemas.create import EmailRequest, VerifyEmail, UserCreate, UserLogin
from app.api.auth.schemas.response import MessageResponse, TokenResponse
from app.api.auth.crud import auth_crud
from util.service_utils import hash_password, verify_password, create_access_token
from util.email_service import generate_verification_code, send_verification_email  


SEND_COOLDOWN_SECONDS = 60       
CODE_EXPIRES_MINUTES = 10        


async def _validate_password(password: str):
    if len(password) < 8:
        raise HTTPException(400, "Пароль должен содержать минимум 8 символов.")
    if not re.search(r"[A-Za-z]", password):
        raise HTTPException(400, "Пароль должен содержать хотя бы одну букву.")
    if not re.search(r"\d", password):
        raise HTTPException(400, "Пароль должен содержать хотя бы одну цифру.")


async def bll_send_verification_code(req: EmailRequest, db: AsyncSession) -> MessageResponse:
    existing_user = await auth_crud.dal_get_user_by_email(req.email, db)
    if existing_user:
        raise HTTPException(status_code=409, detail="Пользователь с таким email уже зарегистрирован")

    ue = await auth_crud.dal_get_user_email_by_email(req.email, db)
    if ue and (datetime.utcnow() - ue.created_at).total_seconds() < SEND_COOLDOWN_SECONDS:
        raise HTTPException(status_code=429, detail="Слишком частые запросы. Попробуйте позже")

    code = int(await generate_verification_code(6))
    ue = await auth_crud.dal_upsert_verification_code(email=req.email, code=code, db=db)

    await send_verification_email(req.email, str(code))

    return MessageResponse(status_code=200, message="Verification code sent")


async def bll_verify_email(req: VerifyEmail, db: AsyncSession) -> MessageResponse:
    if not req.code.isdigit():
        raise HTTPException(400, detail="Некорректный код")

    ue = await auth_crud.dal_get_user_email_by_code(int(req.code), db)
    if not ue:
        raise HTTPException(400, detail="Неверный код")

    if datetime.utcnow() > ue.created_at + timedelta(minutes=CODE_EXPIRES_MINUTES):
        raise HTTPException(400, detail="Срок действия кода истёк")

    ue = await auth_crud.dal_clear_verification_code(ue.id, db)

    return MessageResponse(status_code=200, message=str(ue.id))


async def bll_user_register(req: UserCreate, db: AsyncSession) -> MessageResponse:
    await _validate_password(req.password)

    ue = await auth_crud.dal_get_user_email_by_email(
        email=None, db=db
    )

    from sqlalchemy import select
    res = await db.execute(select(UserEmail).where(UserEmail.id == req.user_email_id))
    ue = res.scalar_one_or_none()

    if not ue:
        raise HTTPException(400, detail="user_email_id не найден")

    if ue.code is not None:
        raise HTTPException(400, detail="Email не подтверждён")

    exists_user = await auth_crud.dal_get_user_by_user_email_id(req.user_email_id, db)
    if exists_user:
        raise HTTPException(409, detail="Пользователь уже создан")

    data = req.dict()
    data["password"] = hash_password(req.password)

    await auth_crud.dal_create_user(data=data, db=db)
    return MessageResponse(status_code=201, message="User registered successfully")


async def bll_user_login(req: UserLogin, db: AsyncSession) -> TokenResponse:
    user = await auth_crud.dal_get_user_by_email(req.email, db)
    if not user:
        raise HTTPException(401, detail="Invalid email or password")

    if not verify_password(req.password, user.password):
        raise HTTPException(401, detail="Invalid email or password")

    token, expire_time = create_access_token({"sub": user.id})
    return TokenResponse(access_token=token, access_token_expire_time=expire_time)