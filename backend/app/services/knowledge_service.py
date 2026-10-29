# import hashlib
# from datetime import datetime, timezone

# from bson import ObjectId
# from fastapi import UploadFile

# from app.database.mongodb import (
#     knowledge_chunks_collection,
#     knowledge_documents_collection,
#     knowledge_files,
# )
# from app.services.embedding_service import (
#     generate_embedding,
# )
# from app.services.pdf_processor import process_pdf

# # Only PDF files are allowed in the knowledge base
# ALLOWED_CONTENT_TYPE = "application/pdf"


# async def _find_duplicate_document(
#     dataset_id: str,
#     user_id: str,
#     file_hash: str,
# ):
#     # Check documents that already have a stored hash first
#     existing_document = await knowledge_documents_collection.find_one(
#         {
#             "dataset_id": dataset_id,
#             "user_id": user_id,
#             "file_hash": file_hash,
#         }
#     )

#     if existing_document:
#         return existing_document

#     # Older documents may not have a file_hash because they were uploaded
#     # before duplicate protection was added
#     cursor = knowledge_documents_collection.find(
#         {
#             "dataset_id": dataset_id,
#             "user_id": user_id,
#         }
#     )

#     documents = await cursor.to_list(length=None)

#     for document in documents:
#         stored_file_hash = document.get("file_hash")

#         # Documents that already have a hash were checked above
#         if stored_file_hash:
#             continue

#         file_id = document.get("file_id")

#         if not file_id:
#             continue

#         try:
#             # Read the old PDF from GridFS so its actual contents can be checked
#             stored_file = await knowledge_files.open_download_stream(ObjectId(file_id))

#             stored_file_data = await stored_file.read()

#             stored_hash = hashlib.sha256(stored_file_data).hexdigest()

#             # Save the hash so this document does not need to be downloaded
#             # again during future duplicate checks
#             await knowledge_documents_collection.update_one(
#                 {
#                     "_id": document["_id"],
#                 },
#                 {
#                     "$set": {
#                         "file_hash": stored_hash,
#                     }
#                 },
#             )

#             # The old document contains the exact same PDF
#             if stored_hash == file_hash:
#                 return document

#         except Exception:
#             # Ignore an old document if its GridFS file can no longer be read
#             continue

#     return None


# async def upload_knowledge_document(
#     file: UploadFile,
#     dataset_id: str,
#     user_id: str,
# ):
#     # Make sure the uploaded file is a PDF
#     if file.content_type != ALLOWED_CONTENT_TYPE:
#         raise ValueError("Only PDF files are allowed")

#     # Read the uploaded PDF before storing and processing it
#     file_data = await file.read()

#     if not file_data:
#         raise ValueError("The uploaded PDF is empty")

#     # Create a unique hash for the exact uploaded PDF
#     # The same file contents always produce the same hash
#     file_hash = hashlib.sha256(file_data).hexdigest()

#     # Check both new documents with hashes and older documents without hashes
#     existing_document = await _find_duplicate_document(
#         dataset_id=dataset_id,
#         user_id=user_id,
#         file_hash=file_hash,
#     )

#     if existing_document:
#         raise ValueError("This PDF has already been uploaded for the selected dataset.")

#     # Extract text and split the PDF into chunks
#     processed_pdf = process_pdf(file_data)

#     # Store the actual PDF file in the knowledge_files GridFS bucket
#     file_id = await knowledge_files.upload_from_stream(
#         file.filename,
#         file_data,
#         metadata={
#             "dataset_id": dataset_id,
#             "user_id": user_id,
#             "content_type": file.content_type,
#             "file_hash": file_hash,
#             "page_count": processed_pdf["page_count"],
#             "chunk_count": processed_pdf["chunk_count"],
#         },
#     )

#     # Store information about the PDF separately from the actual file
#     document = {
#         "dataset_id": dataset_id,
#         "user_id": user_id,
#         "filename": file.filename,
#         "content_type": file.content_type,
#         "file_id": str(file_id),
#         "file_hash": file_hash,
#         "file_size": len(file_data),
#         "page_count": processed_pdf["page_count"],
#         "chunk_count": processed_pdf["chunk_count"],
#         "uploaded_at": datetime.now(timezone.utc),
#         "status": "processed",
#     }

#     result = await knowledge_documents_collection.insert_one(document)

#     # Use the MongoDB document ID to connect every chunk to its PDF
#     document_id = str(result.inserted_id)

#     # Prepare the extracted chunks for MongoDB
#     chunk_documents = []

#     for index, chunk in enumerate(processed_pdf["chunks"]):
#         # Convert each chunk into a vector for semantic search
#         embedding = generate_embedding(chunk)

#         chunk_documents.append(
#             {
#                 "dataset_id": dataset_id,
#                 "user_id": user_id,
#                 "document_id": document_id,
#                 "file_id": str(file_id),
#                 "chunk_index": index,
#                 "text": chunk,
#                 "embedding": embedding,
#             }
#         )

#     # Save all chunks together with their embeddings
#     if chunk_documents:
#         await knowledge_chunks_collection.insert_many(chunk_documents)

#     return {
#         "id": document_id,
#         "dataset_id": dataset_id,
#         "filename": file.filename,
#         "file_id": str(file_id),
#         "file_size": len(file_data),
#         "page_count": processed_pdf["page_count"],
#         "chunk_count": len(chunk_documents),
#         "status": "processed",
#     }







import hashlib
from datetime import datetime, timezone

from bson import ObjectId
from fastapi import UploadFile

from app.database.mongodb import (
    knowledge_chunks_collection,
    knowledge_documents_collection,
    knowledge_files,
)
from app.services.embedding_service import generate_embedding
from app.services.pdf_processor import process_pdf


ALLOWED_CONTENT_TYPE = "application/pdf"


async def _find_duplicate_document(
    dataset_id: str,
    user_id: str,
    file_hash: str,
):
    existing_document = await knowledge_documents_collection.find_one(
        {
            "dataset_id": dataset_id,
            "user_id": user_id,
            "file_hash": file_hash,
        }
    )

    if existing_document:
        return existing_document

    cursor = knowledge_documents_collection.find(
        {
            "dataset_id": dataset_id,
            "user_id": user_id,
        }
    )

    documents = await cursor.to_list(length=None)

    for document in documents:
        stored_file_hash = document.get("file_hash")

        if stored_file_hash:
            continue

        file_id = document.get("file_id")

        if not file_id:
            continue

        try:
            stored_file = await knowledge_files.open_download_stream(
                ObjectId(file_id)
            )

            stored_file_data = await stored_file.read()

            stored_hash = hashlib.sha256(
                stored_file_data
            ).hexdigest()

            await knowledge_documents_collection.update_one(
                {
                    "_id": document["_id"],
                },
                {
                    "$set": {
                        "file_hash": stored_hash,
                    }
                },
            )

            if stored_hash == file_hash:
                return document

        except Exception:
            continue

    return None


async def _delete_existing_knowledge_document(
    dataset_id: str,
    user_id: str,
):
    existing_documents = (
        await knowledge_documents_collection
        .find(
            {
                "dataset_id": dataset_id,
                "user_id": user_id,
            }
        )
        .to_list(length=None)
    )

    for document in existing_documents:
        file_id = document.get("file_id")

        if file_id:
            try:
                await knowledge_files.delete(
                    ObjectId(file_id)
                )
            except Exception:
                pass

    await knowledge_chunks_collection.delete_many(
        {
            "dataset_id": dataset_id,
            "user_id": user_id,
        }
    )

    await knowledge_documents_collection.delete_many(
        {
            "dataset_id": dataset_id,
            "user_id": user_id,
        }
    )


async def upload_knowledge_document(
    file: UploadFile,
    dataset_id: str,
    user_id: str,
):
    if file.content_type != ALLOWED_CONTENT_TYPE:
        raise ValueError("Only PDF files are allowed")

    file_data = await file.read()

    if not file_data:
        raise ValueError("The uploaded PDF is empty")

    file_hash = hashlib.sha256(file_data).hexdigest()

    existing_document = await _find_duplicate_document(
        dataset_id=dataset_id,
        user_id=user_id,
        file_hash=file_hash,
    )

    if existing_document:
        raise ValueError(
            "This PDF has already been uploaded for the selected dataset."
        )

    processed_pdf = process_pdf(file_data)

    await _delete_existing_knowledge_document(
        dataset_id=dataset_id,
        user_id=user_id,
    )

    file_id = None
    document_id = None

    try:
        file_id = await knowledge_files.upload_from_stream(
            file.filename,
            file_data,
            metadata={
                "dataset_id": dataset_id,
                "user_id": user_id,
                "content_type": file.content_type,
                "file_hash": file_hash,
                "page_count": processed_pdf["page_count"],
                "chunk_count": processed_pdf["chunk_count"],
            },
        )

        document = {
            "dataset_id": dataset_id,
            "user_id": user_id,
            "filename": file.filename,
            "content_type": file.content_type,
            "file_id": str(file_id),
            "file_hash": file_hash,
            "file_size": len(file_data),
            "page_count": processed_pdf["page_count"],
            "chunk_count": processed_pdf["chunk_count"],
            "uploaded_at": datetime.now(timezone.utc),
            "status": "processed",
        }

        result = await knowledge_documents_collection.insert_one(
            document
        )

        document_id = str(result.inserted_id)

        chunk_documents = []

        for index, chunk in enumerate(processed_pdf["chunks"]):
            embedding = generate_embedding(chunk)

            chunk_documents.append(
                {
                    "dataset_id": dataset_id,
                    "user_id": user_id,
                    "document_id": document_id,
                    "file_id": str(file_id),
                    "chunk_index": index,
                    "text": chunk,
                    "embedding": embedding,
                }
            )

        if chunk_documents:
            await knowledge_chunks_collection.insert_many(
                chunk_documents
            )

        return {
            "id": document_id,
            "dataset_id": dataset_id,
            "filename": file.filename,
            "file_id": str(file_id),
            "file_size": len(file_data),
            "page_count": processed_pdf["page_count"],
            "chunk_count": len(chunk_documents),
            "status": "processed",
        }

    except Exception:
        if document_id:
            try:
                await knowledge_documents_collection.delete_one(
                    {
                        "_id": ObjectId(document_id),
                    }
                )
            except Exception:
                pass

        if file_id:
            try:
                await knowledge_files.delete(
                    ObjectId(file_id)
                )
            except Exception:
                pass

        if document_id:
            try:
                await knowledge_chunks_collection.delete_many(
                    {
                        "document_id": document_id,
                    }
                )
            except Exception:
                pass

        raise