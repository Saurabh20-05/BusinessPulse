import asyncio
import os

from bson import ObjectId
from dotenv import load_dotenv
from pymongo import AsyncMongoClient
from gridfs.asynchronous import AsyncGridFSBucket


load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
MONGODB_DATABASE = os.getenv(
    "MONGODB_DATABASE",
    "businesspulse",
)

# Duplicate created by the failed duplicate-protection test
DOCUMENT_ID = "6abafb16540bdc009ddfbd5b"
FILE_ID = "6abafb15540bdc009ddfbd59"


async def cleanup_duplicate():
    # Connect to the BusinessPulse database
    client = AsyncMongoClient(MONGODB_URL)
    database = client[MONGODB_DATABASE]

    knowledge_documents = database["knowledge_documents"]
    knowledge_chunks = database["knowledge_chunks"]

    knowledge_files = AsyncGridFSBucket(
        database,
        bucket_name="knowledge_files",
    )

    # Remove chunks belonging to the duplicate document
    chunk_result = await knowledge_chunks.delete_many(
        {
            "document_id": DOCUMENT_ID,
        }
    )

    # Remove the duplicate PDF from GridFS
    await knowledge_files.delete(
        ObjectId(FILE_ID)
    )

    # Remove the duplicate document metadata
    document_result = await knowledge_documents.delete_one(
        {
            "_id": ObjectId(DOCUMENT_ID),
        }
    )

    print(
        f"Chunks removed: {chunk_result.deleted_count}"
    )

    print(
        f"Document removed: {document_result.deleted_count}"
    )

    await client.close()


if __name__ == "__main__":
    asyncio.run(cleanup_duplicate())