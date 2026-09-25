# from app.repositories import dataset_repository


# async def create_dataset(dataset_data: dict):
#     return await dataset_repository.create_dataset(dataset_data)


# async def get_dataset(dataset_id, user_id):
#     return await dataset_repository.find_dataset_by_id(
#         dataset_id,
#         user_id,
#     )


# async def get_user_datasets(user_id: str):
#     return await dataset_repository.find_datasets_by_user(user_id)


# async def delete_dataset(dataset_id, user_id):
#     return await dataset_repository.delete_dataset(
#         dataset_id,
#         user_id,
#     )


# async def update_dataset_mapping(
#     dataset_id: str,
#     user_id: str,
#     mapping: dict,
#     normalized_data: list,
# ):
#     return await dataset_repository.update_dataset_mapping(
#         dataset_id,
#         user_id,
#         mapping,
#         normalized_data,
#     )





from app.repositories import dataset_repository
from app.utils.data_loader import clear_custom_dataset_cache


async def create_dataset(dataset_data: dict):
    return await dataset_repository.create_dataset(
        dataset_data
    )


async def get_dataset(
    dataset_id: str,
    user_id: str,
):
    return await dataset_repository.find_dataset_by_id(
        dataset_id,
        user_id,
    )


async def get_user_datasets(user_id: str):
    return await dataset_repository.find_datasets_by_user(
        user_id
    )


async def delete_dataset(
    dataset_id: str,
    user_id: str,
):
    result = await dataset_repository.delete_dataset(
        dataset_id,
        user_id,
    )

    if result is not None and result.deleted_count > 0:
        clear_custom_dataset_cache(
            dataset_id,
            user_id,
        )

    return result


async def update_dataset_mapping(
    dataset_id: str,
    user_id: str,
    mapping: dict,
    normalized_file_id,
):
    result = await dataset_repository.update_dataset_mapping(
        dataset_id,
        user_id,
        mapping,
        normalized_file_id,
    )

    if result.matched_count > 0:
        clear_custom_dataset_cache(
            dataset_id,
            user_id,
        )

    return result


async def upload_file_to_gridfs(
    filename: str,
    file_data: bytes,
    metadata: dict | None = None,
):
    return await dataset_repository.upload_file_to_gridfs(
        filename,
        file_data,
        metadata,
    )


async def get_file_from_gridfs(file_id):
    return await dataset_repository.get_file_from_gridfs(
        file_id
    )