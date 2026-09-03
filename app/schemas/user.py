from pydantic import BaseModel, EmailStr, Field

class UserRegisterRequest(BaseModel):
    email: EmailStr = Field(description="user's email address")
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8, max_length=64)

class UserRegisterResponse(BaseModel):
    email: EmailStr = Field()
    username: str = Field()

class UserLoginRequest(BaseModel):
    email: EmailStr = Field(description="user's email address")
    password: str = Field(min_length=8, max_length=16)

class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str # added refresh token to the response
    token_type: str = "bearer"

class UserRefreshTokenRequest(BaseModel):
    refresh_token: str = Field(description="user's refresh token")