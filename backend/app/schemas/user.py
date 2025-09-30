from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    phone_number: Optional[str] = None


class UserCreate(UserBase):
    password: Optional[str] = None  # Optional for Google auth
    firebase_uid: Optional[str] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    profile_picture_url: Optional[str] = None


class UserInDB(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    firebase_uid: Optional[str] = None
    profile_picture_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class User(UserInDB):
    pass


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class GoogleAuthRequest(BaseModel):
    firebase_token: str
