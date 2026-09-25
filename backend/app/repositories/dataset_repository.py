# from app.database.mongodb import database

# datasets_collection = database["datasets"]


# async def create_dataset(dataset_data: dict):
#     result = await datasets_collection.insert_one(dataset_data)

#     dataset_data["_id"] = result.inserted_id

#     return dataset_data


# async def find_dataset_by_id(dataset_id: str, user_id: str):
#     return await datasets_collection.find_one(
#         {
#             "dataset_id": dataset_id,
#             "user_id": user_id,
#         }
#     )


# # async def find_datasets_by_user(user_id: str):
# #     cursor = datasets_collection.find(
# #         {"user_id": user_id},
# #         {"_id": 0},
# #     )

# #     return await cursor.to_list(length=None)


# # Return only the dataset details needed by the frontend
# async def find_datasets_by_user(user_id: str):
#     cursor = datasets_collection.find(
#         {"user_id": user_id},
#         {
#             "_id": 0,
#             "dataset_id": 1,
#             "filename": 1,
#             "rows": 1,
#             "columns": 1,
#             "mapping": 1,
#         },
#     )

#     return await cursor.to_list(length=None)


# async def delete_dataset(dataset_id, user_id):
#     return await datasets_collection.delete_one(
#         {
#             "dataset_id": dataset_id,
#             "user_id": user_id,
#         }
#     )


# # Save the column mapping and normalized dataset
# async def update_dataset_mapping(
#     dataset_id: str,
#     user_id: str,
#     mapping: dict,
#     normalized_data: list,
# ):
#     result = await datasets_collection.update_one(
#         {
#             "dataset_id": dataset_id,
#             "user_id": user_id,
#         },
#         {
#             "$set": {
#                 "mapping": mapping,
#                 "normalized_data": normalized_data,
#             }
#         },
#     )

#     print("Dataset ID:", dataset_id)
#     print("Matched:", result.matched_count)
#     print("Modified:", result.modified_count)

#     return result




from bson import ObjectId

from app.database.mongodb import (
    database,
    dataset_files,
)


datasets_collection = database["datasets"]


async def create_dataset(dataset_data: dict):
    """
    Store dataset metadata in MongoDB.
    The actual CSV file is stored separately in GridFS.
    """
    result = await datasets_collection.insert_one(dataset_data)

    dataset_data["_id"] = result.inserted_id

    return dataset_data


async def find_dataset_by_id(
    dataset_id: str,
    user_id: str,
):
    """
    Find a dataset using dataset_id and user_id.
    Only metadata is stored in the datasets collection.
    """
    return await datasets_collection.find_one(
        {
            "dataset_id": dataset_id,
            "user_id": user_id,
        }
    )


async def find_datasets_by_user(user_id: str):
    """
    Return only the dataset metadata needed by the frontend.
    """
    cursor = datasets_collection.find(
        {"user_id": user_id},
        {
            "_id": 0,
            "dataset_id": 1,
            "filename": 1,
            "rows": 1,
            "columns": 1,
            "mapping": 1,
        },
    )

    return await cursor.to_list(length=None)


async def delete_gridfs_file(file_id):
    """
    Delete a file from GridFS if the file exists.
    """
    if not file_id:
        return

    try:
        if isinstance(file_id, str):
            file_id = ObjectId(file_id)

        await dataset_files.delete(file_id)

    except Exception as exc:
        print("GridFS file deletion warning:", exc)


async def delete_dataset(
    dataset_id: str,
    user_id: str,
):
    """
    Delete dataset metadata and associated GridFS files.
    """
    dataset = await find_dataset_by_id(
        dataset_id,
        user_id,
    )

    if not dataset:
        return None

    original_file_id = dataset.get("file_id")
    normalized_file_id = dataset.get("normalized_file_id")

    result = await datasets_collection.delete_one(
        {
            "dataset_id": dataset_id,
            "user_id": user_id,
        }
    )

    # Delete original CSV from GridFS
    await delete_gridfs_file(original_file_id)

    # Delete normalized CSV from GridFS
    if normalized_file_id:
        await delete_gridfs_file(normalized_file_id)

    return result


async def update_dataset_mapping(
    dataset_id: str,
    user_id: str,
    mapping: dict,
    normalized_file_id,
):
    """
    Save the column mapping and reference the normalized CSV
    stored in GridFS.
    """
    result = await datasets_collection.update_one(
        {
            "dataset_id": dataset_id,
            "user_id": user_id,
        },
        {
            "$set": {
                "mapping": mapping,
                "normalized_file_id": normalized_file_id,
            }
        },
    )

    print("Dataset ID:", dataset_id)
    print("Matched:", result.matched_count)
    print("Modified:", result.modified_count)

    return result


async def upload_file_to_gridfs(
    filename: str,
    file_data: bytes,
    metadata: dict | None = None,
):
    """
    Upload a file to MongoDB GridFS.
    """
    file_id = await dataset_files.upload_from_stream(
        filename,
        file_data,
        metadata=metadata or {},
    )

    return file_id


async def get_file_from_gridfs(file_id):
    """
    Download a complete file from GridFS.
    """
    if not file_id:
        return None

    if isinstance(file_id, str):
        file_id = ObjectId(file_id)

    grid_out = await dataset_files.open_download_stream(
        file_id
    )

    return await grid_out.read()