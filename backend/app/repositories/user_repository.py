# optional is used so that function can either return dict or none
from typing import Optional

# So to convert the string back into MongoDB's ID type when searching by ID
from bson import ObjectId

from app.database.mongodb import users_collection

# To create new user document in MongoDB
async def create_user(
    name: str,
    email: str,
    password_hash: str,
) -> dict:

    user = {
        "name": name,
        "email": email,
        "password_hash": password_hash,
    }

    # To Insert the user document into the MongoDB users collection
    result = await users_collection.insert_one(user)

    # Keep the MongoDB id in the returned user object
    user["_id"] = result.inserted_id

    # returns user when services calls for
    return user


# To find a user in MongoDB using their email address
async def find_user_by_email(
    email: str,
) -> Optional[dict]:

    return await users_collection.find_one(
        {
            "email": email,
        }
    )


# To find a user in MongoDB using their MongoDB ID
async def find_user_by_id(
    user_id: str,
) -> Optional[dict]:

    # Check the id before passing it to MongoDB
    if not ObjectId.is_valid(user_id):
        return None

    return await users_collection.find_one(
        {
            "_id": ObjectId(user_id),
        }
    )
