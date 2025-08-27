import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class LogRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        body = await request.body()
        logger.debug(f"Request body: {body}")
        response = await call_next(request)
        return response