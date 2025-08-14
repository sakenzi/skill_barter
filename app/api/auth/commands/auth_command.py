import re
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.auth.schemas.create import EmailRequest, UserCreate, UserLogin
from app.api.auth.schemas.response import TokenResponse, MessageResponse
import random
from util.service_utils import verify_password, create_access_token
