from app.repositories import dataset_repository


async def create_dataset(dataset_data: dict):
    return await dataset_repository.create_dataset(dataset_data)


async def get_dataset(dataset_id, user_id):
    return await dataset_repository.find_dataset_by_id(
        dataset_id,
        user_id,
    )


async def get_user_datasets(user_id: str):
    return await dataset_repository.find_datasets_by_user(user_id)


async def delete_dataset(dataset_id, user_id):
    return await dataset_repository.delete_dataset(
        dataset_id,
        user_id,
    )


async def update_dataset_mapping(
    dataset_id: str,
    user_id: str,
    mapping: dict,
    normalized_data: list,
):
    return await dataset_repository.update_dataset_mapping(
        dataset_id,
        user_id,
        mapping,
        normalized_data,
    )
