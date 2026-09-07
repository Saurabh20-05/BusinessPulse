from app.database.mongodb import database

datasets_collection = database["datasets"]


async def create_dataset(dataset_data: dict):
    result = await datasets_collection.insert_one(dataset_data)

    dataset_data["_id"] = result.inserted_id

    return dataset_data


async def find_dataset_by_id(dataset_id: str, user_id: str):
    return await datasets_collection.find_one(
        {
            "dataset_id": dataset_id,
            "user_id": user_id,
        }
    )


# async def find_datasets_by_user(user_id: str):
#     cursor = datasets_collection.find(
#         {"user_id": user_id},
#         {"_id": 0},
#     )

#     return await cursor.to_list(length=None)


# Return only the dataset details needed by the frontend
async def find_datasets_by_user(user_id: str):
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


async def delete_dataset(dataset_id, user_id):
    return await datasets_collection.delete_one(
        {
            "dataset_id": dataset_id,
            "user_id": user_id,
        }
    )


# Save the column mapping and normalized dataset
async def update_dataset_mapping(
    dataset_id: str,
    user_id: str,
    mapping: dict,
    normalized_data: list,
):
    result = await datasets_collection.update_one(
        {
            "dataset_id": dataset_id,
            "user_id": user_id,
        },
        {
            "$set": {
                "mapping": mapping,
                "normalized_data": normalized_data,
            }
        },
    )

    print("Dataset ID:", dataset_id)
    print("Matched:", result.matched_count)
    print("Modified:", result.modified_count)

    return result
