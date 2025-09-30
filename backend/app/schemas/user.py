"""
User-related Pydantic models for API data contracts
"""
from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """JWT token response model"""
    access_token: str
    token_type: str


class UserBase(BaseModel):
    """Base user model with common fields"""
    username: str


class UserCreate(UserBase):
    """User creation model"""
    password: str


class User(UserBase):
    """User response model (without password)"""
    id: int

    class Config:
        from_attributes = True