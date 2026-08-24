from fastapi import HTTPException, status
#provides ability to return proper HTTP errors

# To interact with MongoDB
from app.repositories.user_repository import (
    create_user,
    find_user_by_email,
    find_user_by_id,
)


from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)


async def signup(
    name: str,
    email: str,
    password: str,
) -> dict:

    # Check if the email is already in use
    existing_user = await find_user_by_email(email)

    # If already a user
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered.",
        )

    # Store only the hashed version of the password
    password_hash = hash_password(password)

    # Creates MongoDB user
    user = await create_user(
        name=name,
        email=email,
        password_hash=password_hash,
    )

    # To return signup response / user information
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
    }


async def login(
    email: str,
    password: str,
) -> dict:

    # To find the user
    user = await find_user_by_email(email)

    # If user doesn't exist
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    # Compare the entered password with the stored hash
    password_is_valid = verify_password(
        password,
        user["password_hash"],
    )

    # If entered password is wrong
    if not password_is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    # If user id and password are correct, we generate JWT (this contains info by which application identifies which user is authenticated)
    access_token = create_access_token(str(user["_id"]))

    # Return the token used for authenticated requests
    # Sends token back to React
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

# When application wants to know which user is logged in
async def get_current_user(
    token: str,
) -> dict:

    # Decode the JWT which comes from frontend
    payload = decode_access_token(token)

    # The user id is stored in the token's "sub" field
    user_id = payload["sub"]

    # After extracting user id, Find that user in MongoDB
    user = await find_user_by_id(user_id)

    # If user doesn't exist
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    # If user exists, return information
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
    }
