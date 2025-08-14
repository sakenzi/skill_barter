from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.auth.commands import auth_command
from db.database import get_db
from app.api.auth.schemas.create import EmailRequest, VerifyEmail, UserCreate, UserLogin
from app.api.auth.schemas.response import TokenResponse, MessageResponse


router = APIRouter()

@router.post(
    "/email/send",
    response_model=MessageResponse,
    summary="Отправка почты"
)
async def send_verification_email(req: EmailRequest, db: AsyncSession = Depends(get_db)):
    return await auth_command.bll_send_verification_email(req, db)


@router.post(
    "/email/verify",
    response_model=MessageResponse,
    summary="Верификация почты"
)
async def verify_email(req: VerifyEmail, db: AsyncSession = Depends(get_db)):
    return await auth_command.bll_verify_email(req, db)


@router.post(
    "/user/register",
    response_model=MessageResponse,
    summary="Регистрация"
)
async def register_user(req: UserCreate, db: AsyncSession = Depends(get_db)):
    return await auth_command.bll_register_user(req, db)


@router.post(
    "/user/login",
    response_model=TokenResponse,
    summary="Логин"
)
async def login_user(req: UserLogin, db: AsyncSession = Depends(get_db)):
    return await auth_command.bll_user_login(req, db)