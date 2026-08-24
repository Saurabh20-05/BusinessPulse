# Used to combine the type of the token with FastAPI's dependency information
from typing import Annotated

# So that before running the function, tells to first obtain dependency
from fastapi import Depends
from fastapi import APIRouter, status

# Used for authentication flow
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.schemas.auth import (
    SignupRequest,
    LoginRequest,
    UserResponse,
    TokenResponse,
)

from app.services import auth_service


# To create the router
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Recieves signup requests from frontend
@router.post(
    # /auth/signup
    "/signup",
    response_model=UserResponse,

    # returns when user is successfully created
    status_code=status.HTTP_201_CREATED,
    summary="Create User Account",
    description="Creates a new user account and stores the securely hashed password in MongoDB.",
)

# to validate incoming JSON from frontend
async def signup(
    data: SignupRequest,
):

    # To pass data to auth_services 
    return await auth_service.signup(
        name=data.name,
        email=data.email,
        password=data.password,
    )


@router.post(

    # /auth/login
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="User Login",
    description="Authenticates a user using email and password and returns a JWT access token.",
)

# validates incoming login JSON from frontend
async def login(
    data: LoginRequest,
):

    # passes data to auth_services
    return await auth_service.login(
        email=data.email,
        password=data.password,
    )

# for swagger OAUTH2 authentication
@router.post(
    "/token",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="OAuth2 Login",
    description="OAuth2-compatible login endpoint used by Swagger authentication.",
)

async def token(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
):
    # Swagger sends the login details through this form
    return await auth_service.login(
        email=form_data.username,
        password=form_data.password,
    )

# to know who is currently authenticated
@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Current User",
    description="Returns the currently authenticated user's information using the JWT access token.",
)

async def get_me(
    token: Annotated[ # Get the JWT token from the Authorization header
        str,
        Depends(oauth2_scheme),
    ],
):
    # Validate the token and get the logged-in user's details
    return await auth_service.get_current_user(token)
