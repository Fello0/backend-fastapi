from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    user_id: int
    role: str


class UserBase(BaseModel):
    username: str
    role: str = "cliente1"


class UserCreate(UserBase):
    password: str = Field(..., min_length=4, max_length=100)


class UserResponse(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True


class UserCreatedResponse(UserResponse):
    message: str
