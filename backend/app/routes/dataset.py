# import io
# import uuid
# import pandas as pd

# from fastapi import APIRouter, Depends, UploadFile, File, HTTPException

# from app.utils.auth import get_authenticated_user
# from app.utils.data_validation import validate_csv_file
# from app.services import dataset_service
# from app.schemas.dataset import DatasetConfigureRequest

# from app.services.dataset_data_service import normalize_dataset

# router = APIRouter(
#     prefix="/dataset",
#     tags=["Dataset"],
#     dependencies=[Depends(get_authenticated_user)],
# )


# # Upload and store a user's CSV dataset
# @router.post("/upload")
# async def upload_dataset(
#     file: UploadFile = File(...),
#     current_user: dict = Depends(get_authenticated_user),
# ):
#     validate_csv_file(file)

#     contents = await file.read()

#     if not contents.strip():
#         raise HTTPException(
#             status_code=400,
#             detail="The uploaded CSV file is empty.",
#         )

#     df = pd.read_csv(io.BytesIO(contents))

#     dataset_id = str(uuid.uuid4())

#     dataset_data = {
#         "dataset_id": dataset_id,
#         "user_id": current_user["id"],
#         "filename": file.filename,
#         "rows": len(df),
#         "columns": df.columns.tolist(),
#         "mapping": {},
#         "data": df.to_dict(orient="records"),
#     }

#     await dataset_service.create_dataset(dataset_data)

#     return {
#         "message": "Dataset uploaded successfully.",
#         "dataset_id": dataset_id,
#         "filename": file.filename,
#         "rows": len(df),
#         "columns": df.columns.tolist(),
#         "preview": df.head(5).fillna("").to_dict(orient="records"),
#     }


# # Save the column mapping and normalized dataset
# @router.post("/configure")
# async def configure_dataset(
#     request: DatasetConfigureRequest,
#     current_user: dict = Depends(get_authenticated_user),
# ):
#     dataset = await dataset_service.get_dataset(
#         request.dataset_id,
#         current_user["id"],
#     )

#     if not dataset:
#         raise HTTPException(
#             status_code=404,
#             detail="Dataset not found.",
#         )

#     if dataset["user_id"] != current_user["id"]:
#         raise HTTPException(
#             status_code=403,
#             detail="You do not have access to this dataset.",
#         )

#     df = pd.DataFrame(dataset["data"])

#     normalized_df = normalize_dataset(
#         df,
#         request.mapping,
#     )

#     await dataset_service.update_dataset_mapping(
#         request.dataset_id,
#         current_user["id"],
#         request.mapping,
#         normalized_df.to_dict(orient="records"),
#     )

#     return {
#         "message": "Dataset mapping saved successfully.",
#         "dataset_id": request.dataset_id,
#         "mapping": request.mapping,
#         "normalized_columns": normalized_df.columns.tolist(),
#     }


# # Return all datasets uploaded by the current user
# @router.get("")
# async def get_my_datasets(
#     current_user: dict = Depends(get_authenticated_user),
# ):
#     datasets = await dataset_service.get_user_datasets(current_user["id"])

#     return datasets


# # Return a preview of the selected dataset
# @router.get("/{dataset_id}/preview")
# async def preview_dataset(
#     dataset_id: str,
#     current_user=Depends(get_authenticated_user),
# ):
#     dataset = await dataset_service.get_dataset(
#         dataset_id,
#         current_user["id"],
#     )

#     if not dataset:
#         raise HTTPException(
#             status_code=404,
#             detail="Dataset not found.",
#         )

#     original_data = dataset.get("data", [])

#     return {
#         "dataset_id": dataset["dataset_id"],
#         "filename": dataset["filename"],
#         "rows": dataset["rows"],
#         "columns": dataset["columns"],
#         "preview": original_data[:5],
#     }


# # Delete the selected dataset for the current user
# @router.delete("/{dataset_id}")
# async def delete_dataset(
#     dataset_id: str,
#     current_user: dict = Depends(get_authenticated_user),
# ):
#     deleted = await dataset_service.delete_dataset(
#         dataset_id,
#         current_user["id"],
#     )

#     if deleted.deleted_count == 0:
#         raise HTTPException(
#             status_code=404,
#             detail="Dataset not found.",
#         )

#     return {
#         "message": "Dataset deleted successfully.",
#         "dataset_id": dataset_id,
#     }











import io
import uuid

import pandas as pd

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException,
)

from app.utils.auth import get_authenticated_user
from app.utils.data_validation import validate_csv_file
from app.services import dataset_service
from app.schemas.dataset import DatasetConfigureRequest

from app.services.dataset_data_service import normalize_dataset


router = APIRouter(
    prefix="/dataset",
    tags=["Dataset"],
    dependencies=[Depends(get_authenticated_user)],
)


# Upload and store a user's CSV dataset
@router.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_authenticated_user),
):
    validate_csv_file(file)

    contents = await file.read()

    if not contents.strip():
        raise HTTPException(
            status_code=400,
            detail="The uploaded CSV file is empty.",
        )

    try:
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to read CSV file: {str(exc)}",
        )

    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="The uploaded CSV file contains no data.",
        )

    dataset_id = str(uuid.uuid4())

    # Store the actual CSV file in GridFS
    file_id = await dataset_service.upload_file_to_gridfs(
        filename=file.filename,
        file_data=contents,
        metadata={
            "dataset_id": dataset_id,
            "user_id": current_user["id"],
            "file_type": "original",
        },
    )

    # Store only metadata in MongoDB
    dataset_data = {
        "dataset_id": dataset_id,
        "user_id": current_user["id"],
        "filename": file.filename,
        "rows": len(df),
        "columns": df.columns.tolist(),
        "mapping": {},
        "file_id": file_id,
    }

    try:
        await dataset_service.create_dataset(dataset_data)
    except Exception:
        # Clean up GridFS file if metadata creation fails
        from app.repositories import dataset_repository

        await dataset_repository.delete_gridfs_file(file_id)
        raise

    return {
        "message": "Dataset uploaded successfully.",
        "dataset_id": dataset_id,
        "filename": file.filename,
        "rows": len(df),
        "columns": df.columns.tolist(),
        "preview": (
            df.head(5)
            .fillna("")
            .to_dict(orient="records")
        ),
    }


# Save the column mapping and normalized dataset
@router.post("/configure")
async def configure_dataset(
    request: DatasetConfigureRequest,
    current_user: dict = Depends(get_authenticated_user),
):
    dataset = await dataset_service.get_dataset(
        request.dataset_id,
        current_user["id"],
    )

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found.",
        )

    if dataset["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this dataset.",
        )

    file_id = dataset.get("file_id")

    if not file_id:
        raise HTTPException(
            status_code=400,
            detail="Dataset file is not available.",
        )

    # Download the original CSV from GridFS
    contents = await dataset_service.get_file_from_gridfs(
        file_id
    )

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Unable to read dataset file.",
        )

    try:
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to read dataset file: {str(exc)}",
        )

    # Normalize the dataset using the selected mapping
    normalized_df = normalize_dataset(
        df,
        request.mapping,
    )

    # Convert normalized DataFrame to CSV
    normalized_csv = normalized_df.to_csv(
        index=False
    ).encode("utf-8")

    # Store normalized CSV in GridFS
    normalized_file_id = (
        await dataset_service.upload_file_to_gridfs(
            filename=f"{dataset['filename']}_normalized.csv",
            file_data=normalized_csv,
            metadata={
                "dataset_id": request.dataset_id,
                "user_id": current_user["id"],
                "file_type": "normalized",
            },
        )
    )

    old_normalized_file_id = dataset.get(
        "normalized_file_id"
    )

    try:
        await dataset_service.update_dataset_mapping(
            request.dataset_id,
            current_user["id"],
            request.mapping,
            normalized_file_id,
        )
    except Exception:
        # Clean up newly uploaded file if metadata update fails
        from app.repositories import dataset_repository

        await dataset_repository.delete_gridfs_file(
            normalized_file_id
        )
        raise

    # Remove previous normalized file after successful update
    if old_normalized_file_id:
        from app.repositories import dataset_repository

        await dataset_repository.delete_gridfs_file(
            old_normalized_file_id
        )

    return {
        "message": "Dataset mapping saved successfully.",
        "dataset_id": request.dataset_id,
        "mapping": request.mapping,
        "normalized_columns": normalized_df.columns.tolist(),
    }


# Get all datasets belonging to the current user
@router.get("")
async def get_my_datasets(
    current_user: dict = Depends(get_authenticated_user),
):
    datasets = await dataset_service.get_user_datasets(
        current_user["id"]
    )

    return datasets


# Get dataset preview
@router.get("/{dataset_id}/preview")
async def preview_dataset(
    dataset_id: str,
    current_user=Depends(get_authenticated_user),
):
    dataset = await dataset_service.get_dataset(
        dataset_id,
        current_user["id"],
    )

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found.",
        )

    file_id = dataset.get("file_id")

    if not file_id:
        raise HTTPException(
            status_code=400,
            detail="Dataset file is not available.",
        )

    # Read the CSV stored in GridFS
    contents = await dataset_service.get_file_from_gridfs(
        file_id
    )

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Unable to read dataset file.",
        )

    try:
        preview_df = pd.read_csv(
            io.BytesIO(contents),
            nrows=5,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to read dataset file: {str(exc)}",
        )

    return {
        "dataset_id": dataset["dataset_id"],
        "filename": dataset["filename"],
        "rows": dataset["rows"],
        "columns": dataset["columns"],
        "preview": (
            preview_df
            .fillna("")
            .to_dict(orient="records")
        ),
    }


# Delete dataset
@router.delete("/{dataset_id}")
async def delete_dataset(
    dataset_id: str,
    current_user=Depends(get_authenticated_user),
):
    deleted = await dataset_service.delete_dataset(
        dataset_id,
        current_user["id"],
    )

    if deleted is None or deleted.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found.",
        )

    return {
        "message": "Dataset deleted successfully.",
        "dataset_id": dataset_id,
    }