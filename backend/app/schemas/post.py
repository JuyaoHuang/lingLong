"""
Post-related Pydantic models for API data contracts
Must match the Astro frontend content.config.ts schema exactly
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


class PostMetadata(BaseModel):
    """
    Post metadata model - matches frontend AdminPostCard.astro Props interface
    Used for article list display without content body
    """
    slug: str
    title: str
    published: date  # 保持date格式，与前端AdminPostCard.astro Props一致
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    first_level_category: str
    second_level_category: str
    author: Optional[str] = None
    draft: Optional[bool] = False
    cover: Optional[str] = None
    sourceLink: Optional[str] = None
    licenseName: Optional[str] = None
    licenseUrl: Optional[str] = None


class PostCreate(BaseModel):
    """
    Post creation model - for creating new articles
    Content field separated from metadata
    """
    title: str
    content: str
    published: date  # 保持date格式
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    first_level_category: str
    second_level_category: str
    author: Optional[str] = None
    draft: Optional[bool] = False
    cover: Optional[str] = None
    sourceLink: Optional[str] = None
    licenseName: Optional[str] = None
    licenseUrl: Optional[str] = None


class PostUpdate(BaseModel):
    """
    Post update model - for updating existing articles
    All fields optional to allow partial updates
    """
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[date] = None  # 保持date格式
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    first_level_category: Optional[str] = None
    second_level_category: Optional[str] = None
    author: Optional[str] = None
    draft: Optional[bool] = None
    cover: Optional[str] = None
    sourceLink: Optional[str] = None
    licenseName: Optional[str] = None
    licenseUrl: Optional[str] = None


class PostFull(PostMetadata):
    """
    Complete post model - includes content body
    Used for article detail view and editing
    """
    content: str


class PostResponse(BaseModel):
    """
    Standard API response for post operations
    """
    success: bool
    message: str
    data: Optional[dict] = None