from pydantic import BaseModel, EmailStr, Field


# TO DEFINE WHAT DATA API ACCEPTS AND WHAT DATA IT RETURNS

# Defines data expected when a user signs up
class SignupRequest(BaseModel):

    # Name validation
    name: str = Field(
        min_length=2,
        max_length=100,
        description="User's full name",
    )

    # email validation
    email: EmailStr = Field(
        description="User's email address",
    )

    # password validation
    password: str = Field(
        min_length=8,
        max_length=128,
        description="User's password",
    )


# Defines the data expected during normal frontend login
class LoginRequest(BaseModel):
    email: EmailStr = Field(
        description="User's email address",
    )

    password: str = Field(
        min_length=8,
        max_length=128,
        description="User's password",
    )


# Defines what user information your API returns to the frontend
class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
# This is used in routes in signup


# Defines what the login endpoint returns after successful authentication
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
