
import logging
from datetime import datetime, timezone

import certifi
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from config import config

logger = logging.getLogger(__name__)

_client = None


def _get_collection():
    global _client
    if _client is None:
        _client = MongoClient(
            config.MONGODB_URI,
            serverSelectionTimeoutMS=5000,
            tlsCAFile=certifi.where(),
        )
    return _client[config.MONGODB_DB_NAME]["scans"]


def save_scan(label_text: str, advice: str, source: str, age: int, conditions: str):
    """Persist one scan. Returns the inserted id as a string, or None on failure."""
    document = {
        "label_text": label_text,
        "advice": advice,
        "source": source,
        "age": age,
        "conditions": conditions,
        "created_at": datetime.now(timezone.utc),
    }
    try:
        result = _get_collection().insert_one(document)
        return str(result.inserted_id)
    except PyMongoError as exc:
        logger.warning("Could not save scan to MongoDB: %s", exc)
        return None


def get_recent_scans(limit: int = 20):
    """Return the most recent scans, newest first. Empty list if DB is down."""
    try:
        cursor = _get_collection().find().sort("created_at", -1).limit(limit)
        scans = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            doc["created_at"] = doc["created_at"].isoformat()
            scans.append(doc)
        return scans
    except PyMongoError as exc:
        logger.warning("Could not fetch scan history from MongoDB: %s", exc)
        return []
