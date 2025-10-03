"""
用于 API 数据契约的用户相关 Pydantic 模型
User-related Pydantic models for API data contracts
"""
from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """JWT 令牌响应模型--JWT token response model"""
    access_token: str
    token_type: str


class UserBase(BaseModel):
    """具有公共字段的基本用户模型--Base user model with common fields"""
    username: str


class UserCreate(UserBase):
    """用户创建模型--User creation model"""
    password: str


class User(UserBase):
    """用户响应模型（无密码）--User response model (without password)"""
    id: int

    class Config:
        from_attributes = True