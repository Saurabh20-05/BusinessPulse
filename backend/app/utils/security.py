import os
# used when creating the JWT expiration time
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
# for password hashing and password verification.
from pwdlib import PasswordHash

load_dotenv()


JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

# To get the JWT signing algorithm
JWT_ALGORITHM = os.getenv(
    "JWT_ALGORITHM",
    "HS256",
)

# determines how long the JWT remains valid
JWT_EXPIRE_MINUTES = int(
    os.getenv(
        "JWT_EXPIRE_MINUTES",
        "60",
    )
)

# Make sure the app has a secret key before creating tokens
if not JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not configured in the .env file.")

# creates the password hashing utility
password_hash = PasswordHash.recommended()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# Keep password handling in one place for signup and login
# used bu signup to store password as hash
# signup function in services calls this function
def hash_password(password: str) -> str:
    return password_hash.hash(password)

# Used during login
# checks whether entered password is same as hash password
def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return password_hash.verify(
        plain_password,
        hashed_password,
    )

# To create JWT
# this function recieves users ID
def create_access_token(
    user_id: str,
) -> str:

    # Set when the token should expire and which user it belongs to
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)

    payload = {
        "sub": user_id, # subject of token
        "exp": expire, # expiry time of token
    }

    # to encode all into single JWT
    token = jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

    # returns the JWT token
    return token


# To check the JWT
def decode_access_token(
    token: str,
) -> dict:

    # Check the token and get the user id stored inside it
    try:

        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )

        # get user id
        user_id = payload.get("sub")

        # if token does not contain user id
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token.",
                headers={
                    "WWW-Authenticate": "Bearer",
                },
            )

        # if token is valid, payload is returned
        return payload

    # if JWT has passed the expiry time
    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    # if JWT is invalid
    except jwt.InvalidTokenError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )
