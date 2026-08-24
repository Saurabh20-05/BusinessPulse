import os

from dotenv import load_dotenv
from pymongo import AsyncMongoClient

# Get database details from .env
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

# search for database name, if not present, use businesspulse
MONGODB_DATABASE = os.getenv(
    "MONGODB_DATABASE",
    "businesspulse",
)

# Don't start the app if MongoDB URL is missing
if not MONGODB_URL:
    raise RuntimeError(
        "MONGODB_URL is not configured in the .env file."
    )

client = AsyncMongoClient(MONGODB_URL)

# selects database to work with
database = client[MONGODB_DATABASE]

# Collection used for storing users
users_collection = database["users"]