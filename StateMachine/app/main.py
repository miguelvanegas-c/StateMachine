from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware 
from fastapi import FastAPI
from app.config.application_config import settings
from app.routers.order_router import router as order_router
from app.exceptions.handler_exception import register_exception_handlers

import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)
register_exception_handlers(app)
app.include_router(order_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
