import re
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.auth.schemas.create import EmailRequest, UserCreate, UserLogin, VerifyEmail
from app.api.auth.schemas.response import TokenResponse, MessageResponse
import random
from util.service_utils import verify_password, create_access_token
from app.api.auth.crud.auth_crud import (dal_create_email_verification, dal_create_user, dal_get_email_by_code, 
                                         dal_get_user_by_email, dal_mark_email_verified)
from util.email_service import send_email_message


async def bll_send_verification_email(req: EmailRequest, db: AsyncSession):
    code = random.randint(100000, 999999)
    await dal_create_email_verification(req.email, code, db)
    await send_email_message(req.email, "Email Verification", f"Your code: {code}")
    return MessageResponse(status_code=200, message="Verification code sent")


async def bll_verify_email(req: VerifyEmail, db: AsyncSession):
    user_email = await dal_get_email_by_code(int(req.code), db)
    if not user_email:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    await dal_mark_email_verified(user_email, db)
    return MessageResponse(status_code=200, message=str(user_email.id))


async def bll_register_user(req: UserCreate, db: AsyncSession):
    user = await dal_create_user(req.dict(), db)
    return MessageResponse(status_code=201, message="User registered successfully")


async def bll_user_login(req: UserLogin, db: AsyncSession):
    user = await dal_get_user_by_email(req.email, db)
    if not user or not verify_password(req.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token, expire_time = await create_access_token({"sub": user.id})
    return TokenResponse(access_token=token, access_token_expire_time=expire_time)