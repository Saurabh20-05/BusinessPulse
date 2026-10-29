import asyncio
import os

from bson import ObjectId
from dotenv import load_dotenv
from gridfs.asynchronous import AsyncGridFSBucket
from pymongo import AsyncMongoClient


load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
MONGODB_DATABASE = os.getenv(
    "MONGODB_DATABASE",
    "businesspulse",
)


# Keep this document and remove the other duplicate uploads
KEEP_DOCUMENT_ID = "6abaf2213240f8a73abe25b8"

# Duplicate documents that were created by repeated PDF uploads
DUPLICATE_DOCUMENTS = [
    {
        "document_id": "6abaf6b20becd25804e441c1",
        "file_id": "6abaf6b20becd25804e441bf",
    },
    {
        "document_id": "6abaf6cc0becd25804e441c5",
        "file_id": "6abaf6cc0becd25804e441c3",
    },
]


async def cleanup_duplicates():
    # Connect to the same MongoDB database used by BusinessPulse
    client = AsyncMongoClient(MONGODB_URL)
    database = client[MONGODB_DATABASE]

    knowledge_documents = database["knowledge_documents"]
    knowledge_chunks = database["knowledge_chunks"]

    knowledge_files = AsyncGridFSBucket(
        database,
        bucket_name="knowledge_files",
    )

    for duplicate in DUPLICATE_DOCUMENTS:
        document_id = duplicate["document_id"]
        file_id = duplicate["file_id"]

        # Remove all chunks belonging to this duplicate document
        chunk_result = await knowledge_chunks.delete_many(
            {
                "document_id": document_id,
            }
        )

        # Remove the duplicate PDF from GridFS
        await knowledge_files.delete(
            ObjectId(file_id)
        )

        # Remove the duplicate document metadata
        document_result = await knowledge_documents.delete_one(
            {
                "_id": ObjectId(document_id),
            }
        )

        print(
            f"Removed document: {document_id}"
        )

        print(
            f"Chunks removed: {chunk_result.deleted_count}"
        )

        print(
            f"Document removed: {document_result.deleted_count}"
        )

    # Confirm that the document we wanted to keep still exists
    kept_document = await knowledge_documents.find_one(
        {
            "_id": ObjectId(KEEP_DOCUMENT_ID),
        }
    )

    if kept_document:
        print(
            f"Kept document: {KEEP_DOCUMENT_ID}"
        )
    else:
        print(
            "WARNING: The document marked to keep was not found."
        )

    await client.close()


if __name__ == "__main__":
    asyncio.run(cleanup_duplicates())