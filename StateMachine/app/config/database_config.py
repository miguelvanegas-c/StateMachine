from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi
from app.config.application_config import settings

MONGO_URI = settings.MONGO_URI

client: AsyncMongoClient = AsyncMongoClient(
    MONGO_URI,
    server_api=ServerApi(version="1", strict=True, deprecation_errors=True)
)

db = client[settings.MONGO_DB]

async def get_db():
    yield db