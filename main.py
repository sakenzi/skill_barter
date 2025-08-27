from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router import route
from util.log_util import LogRequestMiddleware


app = FastAPI()
app.add_middleware(LogRequestMiddleware)

origins = [
    "http://localhost:3000",
    "http://172.20.10.8:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(route)