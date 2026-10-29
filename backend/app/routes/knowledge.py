# # # # from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

# # # # from app.services.knowledge_service import (
# # # #     upload_knowledge_document,
# # # # )
# # # # from app.utils.auth import get_authenticated_user


# # # # router = APIRouter(
# # # #     prefix="/knowledge",
# # # #     tags=["Knowledge Base"],
# # # #     dependencies=[
# # # #         Depends(get_authenticated_user)
# # # #     ],
# # # # )


# # # # @router.post("/upload")
# # # # async def upload_knowledge_file(
# # # #     dataset_id: str = Form(...),
# # # #     file: UploadFile = File(...),
# # # #     current_user: dict = Depends(
# # # #         get_authenticated_user
# # # #     ),
# # # # ):
# # # #     try:
# # # #         # Store the PDF and its metadata for the logged in user
# # # #         result = await upload_knowledge_document(
# # # #             file=file,
# # # #             dataset_id=dataset_id,
# # # #             user_id=current_user["id"],
# # # #         )

# # # #         return result

# # # #     except ValueError as exc:
# # # #         raise HTTPException(
# # # #             status_code=400,
# # # #             detail=str(exc),
# # # #         )

# # # #     except Exception as exc:
# # # #         raise HTTPException(
# # # #             status_code=500,
# # # #             detail=f"Knowledge file upload failed: {str(exc)}",
# # # #         )




# # # from bson import ObjectId
# # # from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

# # # from app.database.mongodb import (
# # #     knowledge_documents_collection,
# # #     knowledge_chunks_collection,
# # #     knowledge_files,
# # # )
# # # from app.services.knowledge_service import (
# # #     upload_knowledge_document,
# # # )
# # # from app.utils.auth import get_authenticated_user


# # # router = APIRouter(
# # #     prefix="/knowledge",
# # #     tags=["Knowledge Base"],
# # # )


# # # @router.get("/status/{dataset_id}")
# # # async def get_knowledge_status(
# # #     dataset_id: str,
# # #     current_user: dict = Depends(
# # #         get_authenticated_user
# # #     ),
# # # ):
# # #     document = await knowledge_documents_collection.find_one(
# # #         {
# # #             "dataset_id": dataset_id,
# # #             "user_id": current_user["id"],
# # #             "status": "processed",
# # #         },
# # #         {
# # #             "_id": 0,
# # #             "filename": 1,
# # #             "file_id": 1,
# # #             "status": 1,
# # #         },
# # #     )

# # #     if not document:
# # #         return {
# # #             "uploaded": False,
# # #             "filename": None,
# # #             "file_id": None,
# # #             "status": None,
# # #         }

# # #     return {
# # #         "uploaded": True,
# # #         "filename": document.get("filename"),
# # #         "file_id": document.get("file_id"),
# # #         "status": document.get("status"),
# # #     }


# # # @router.post("/upload")
# # # async def upload_knowledge_file(
# # #     dataset_id: str = Form(...),
# # #     file: UploadFile = File(...),
# # #     current_user: dict = Depends(
# # #         get_authenticated_user
# # #     ),
# # # ):
# # #     user_id = current_user["id"]

# # #     try:
# # #         existing_documents = (
# # #             await knowledge_documents_collection
# # #             .find(
# # #                 {
# # #                     "dataset_id": dataset_id,
# # #                     "user_id": user_id,
# # #                 }
# # #             )
# # #             .to_list(length=None)
# # #         )

# # #         for document in existing_documents:
# # #             file_id = document.get("file_id")

# # #             if file_id:
# # #                 try:
# # #                     await knowledge_files.delete(
# # #                         ObjectId(file_id)
# # #                     )
# # #                 except Exception:
# # #                     pass

# # #         await knowledge_chunks_collection.delete_many(
# # #             {
# # #                 "dataset_id": dataset_id,
# # #                 "user_id": user_id,
# # #             }
# # #         )

# # #         await knowledge_documents_collection.delete_many(
# # #             {
# # #                 "dataset_id": dataset_id,
# # #                 "user_id": user_id,
# # #             }
# # #         )

# # #         result = await upload_knowledge_document(
# # #             file=file,
# # #             dataset_id=dataset_id,
# # #             user_id=user_id,
# # #         )

# # #         return result

# # #     except ValueError as exc:
# # #         raise HTTPException(
# # #             status_code=400,
# # #             detail=str(exc),
# # #         )

# # #     except Exception as exc:
# # #         raise HTTPException(
# # #             status_code=500,
# # #             detail=f"Knowledge file upload failed: {str(exc)}",
# # #         )











# # from bson import ObjectId
# # from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

# # from app.database.mongodb import (
# #     knowledge_documents_collection,
# #     knowledge_chunks_collection,
# #     knowledge_files,
# # )
# # from app.services.knowledge_service import upload_knowledge_document
# # from app.utils.auth import get_authenticated_user


# # router = APIRouter(
# #     prefix="/knowledge",
# #     tags=["Knowledge Base"],
# # )


# # @router.get("/status/{dataset_id}")
# # async def get_knowledge_status(
# #     dataset_id: str,
# #     current_user: dict = Depends(get_authenticated_user),
# # ):
# #     document = await knowledge_documents_collection.find_one(
# #         {
# #             "dataset_id": dataset_id,
# #             "user_id": current_user["id"],
# #             "status": "processed",
# #         },
# #         {
# #             "_id": 0,
# #             "filename": 1,
# #             "file_id": 1,
# #             "status": 1,
# #         },
# #     )

# #     if not document:
# #         return {
# #             "uploaded": False,
# #             "filename": None,
# #             "file_id": None,
# #             "status": None,
# #         }

# #     return {
# #         "uploaded": True,
# #         "filename": document.get("filename"),
# #         "file_id": document.get("file_id"),
# #         "status": document.get("status"),
# #     }


# # @router.post("/upload")
# # async def upload_knowledge_file(
# #     dataset_id: str = Form(...),
# #     file: UploadFile = File(...),
# #     current_user: dict = Depends(get_authenticated_user),
# # ):
# #     user_id = current_user["id"]

# #     try:
# #         existing_documents = (
# #             await knowledge_documents_collection
# #             .find(
# #                 {
# #                     "dataset_id": dataset_id,
# #                     "user_id": user_id,
# #                 }
# #             )
# #             .to_list(length=None)
# #         )

# #         for document in existing_documents:
# #             file_id = document.get("file_id")

# #             if file_id:
# #                 try:
# #                     await knowledge_files.delete(
# #                         ObjectId(file_id)
# #                     )
# #                 except Exception:
# #                     pass

# #         await knowledge_chunks_collection.delete_many(
# #             {
# #                 "dataset_id": dataset_id,
# #                 "user_id": user_id,
# #             }
# #         )

# #         await knowledge_documents_collection.delete_many(
# #             {
# #                 "dataset_id": dataset_id,
# #                 "user_id": user_id,
# #             }
# #         )

# #         result = await upload_knowledge_document(
# #             file=file,
# #             dataset_id=dataset_id,
# #             user_id=user_id,
# #         )

# #         return result

# #     except ValueError as exc:
# #         raise HTTPException(
# #             status_code=400,
# #             detail=str(exc),
# #         )

# #     except Exception as exc:
# #         raise HTTPException(
# #             status_code=500,
# #             detail=f"Knowledge file upload failed: {str(exc)}",
# #         )






# from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

# from app.database.mongodb import knowledge_documents_collection
# from app.services.knowledge_service import upload_knowledge_document
# from app.utils.auth import get_authenticated_user


# router = APIRouter(
#     prefix="/knowledge",
#     tags=["Knowledge Base"],
# )


# @router.get("/status/{dataset_id}")
# async def get_knowledge_status(
#     dataset_id: str,
#     current_user: dict = Depends(get_authenticated_user),
# ):
#     document = await knowledge_documents_collection.find_one(
#         {
#             "dataset_id": dataset_id,
#             "user_id": current_user["id"],
#             "status": "processed",
#         },
#         {
#             "_id": 0,
#             "filename": 1,
#             "file_id": 1,
#             "status": 1,
#         },
#     )

#     if not document:
#         return {
#             "uploaded": False,
#             "filename": None,
#             "file_id": None,
#             "status": None,
#         }

#     return {
#         "uploaded": True,
#         "filename": document.get("filename"),
#         "file_id": document.get("file_id"),
#         "status": document.get("status"),
#     }


# @router.post("/upload")
# async def upload_knowledge_file(
#     dataset_id: str = Form(...),
#     file: UploadFile = File(...),
#     current_user: dict = Depends(get_authenticated_user),
# ):
#     try:
#         result = await upload_knowledge_document(
#             file=file,
#             dataset_id=dataset_id,
#             user_id=current_user["id"],
#         )

#         return result

#     except ValueError as exc:
#         raise HTTPException(
#             status_code=400,
#             detail=str(exc),
#         )

#     except Exception as exc:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Knowledge file upload failed: {str(exc)}",
#         )







import hashlib

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.database.mongodb import knowledge_documents_collection
from app.services.knowledge_service import upload_knowledge_document
from app.utils.auth import get_authenticated_user


router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge Base"],
)


@router.get("/status/{dataset_id}")
async def get_knowledge_status(
    dataset_id: str,
    current_user: dict = Depends(get_authenticated_user),
):
    document = await knowledge_documents_collection.find_one(
        {
            "dataset_id": dataset_id,
            "user_id": current_user["id"],
            "status": "processed",
        },
        {
            "_id": 0,
            "filename": 1,
            "file_id": 1,
            "status": 1,
        },
    )

    if not document:
        return {
            "uploaded": False,
            "filename": None,
            "file_id": None,
            "status": None,
        }

    return {
        "uploaded": True,
        "filename": document.get("filename"),
        "file_id": document.get("file_id"),
        "status": document.get("status"),
    }


@router.post("/upload")
async def upload_knowledge_file(
    dataset_id: str = Form(...),
    file: UploadFile = File(...),
    current_user: dict = Depends(get_authenticated_user),
):
    user_id = current_user["id"]

    try:
        file_data = await file.read()

        if not file_data:
            raise ValueError("The uploaded PDF is empty")

        file_hash = hashlib.sha256(file_data).hexdigest()

        existing_document = (
            await knowledge_documents_collection.find_one(
                {
                    "dataset_id": dataset_id,
                    "user_id": user_id,
                    "file_hash": file_hash,
                }
            )
        )

        if existing_document:
            raise ValueError(
                "This PDF has already been uploaded for the selected dataset."
            )

        await file.seek(0)

        result = await upload_knowledge_document(
            file=file,
            dataset_id=dataset_id,
            user_id=user_id,
        )

        return result

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Knowledge file upload failed: {str(exc)}",
        )