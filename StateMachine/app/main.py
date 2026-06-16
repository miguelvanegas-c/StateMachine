from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware 
from fastapi import FastAPI
from app.config import settings
from app.routers.order_router import router as order_router
from app.routers.state_router import router as state_router
from app.routers.event_router import router as event_router
from app.routers.ticket_router import router as ticket_router
from app.exceptions.handler_exception import register_exception_handlers
from app.config.init_db import initialize_db
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_db()
    yield


app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG, lifespan=lifespan)
register_exception_handlers(app)
app.include_router(order_router)
app.include_router(state_router)
app.include_router(event_router)
app.include_router(ticket_router)
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
