# Used to combine the type of the token with FastAPI's dependency information
from typing import Annotated

# So that before running the function, tells to first obtain dependency
from fastapi import Depends

# So that can read bearer token from requests header
from fastapi.security import OAuth2PasswordBearer


from app.services.auth_service import get_current_user

# To create OAUTH2 scheme
# Extracts just the token from the Bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# Used by protected routes to get the logged-in user
async def get_authenticated_user(
    token: Annotated[
        str,
        Depends(oauth2_scheme),
    ],
):

    # Pass the token to the service
    return await get_current_user(token)
