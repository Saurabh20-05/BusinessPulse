# from datetime import datetime

# from pydantic import BaseModel, ConfigDict


# class KnowledgeDocument(BaseModel):
#     model_config = ConfigDict(extra="forbid")

#     dataset_id: str
#     user_id: str
#     filename: str
#     content_type: str
#     file_id: str
#     file_size: int
#     uploaded_at: datetime
#     status: str = "uploaded"


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
    try:
        result = await upload_knowledge_document(
            file=file,
            dataset_id=dataset_id,
            user_id=current_user["id"],
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