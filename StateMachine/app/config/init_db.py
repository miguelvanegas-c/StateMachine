import json
from pathlib import Path
from app.config.database_config import db
import logging

logger = logging.getLogger(__name__)

async def initialize_db():
    await init_collection( collection_name="events", path="events_startup.json")
    await init_collection(collection_name="states",path="states_startup.json")

async def init_collection(collection_name:str, path:str):
    collection = db[collection_name]
    count = await collection.count_documents({})
    if count == 0:
        json_path = Path(__file__).parent / "data" / path
        if not json_path.exists():
            logger.info(f"Initialization file not found: {json_path}")
            return

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if data:
            await collection.insert_many(data)
            logger.info(f"Collection 'events' initialized with {len(data)} documents.")
        else:
            logger.info("JSON file is empty. No data inserted.")
    else:
        logger.info(f"Collection {collection_name} already contains {count} documents. Initialization skipped")