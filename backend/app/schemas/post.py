"""
后置相关的 Pydantic API 数据契约模型
必须与 Astro 前端 content.config.ts 架构完全匹配
Post-related Pydantic models for API data contracts
Must match the Astro frontend content.config.ts schema exactly
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


class PostMetadata(BaseModel):
    """
    帖子元数据模型 - 匹配前端 AdminPostCard.astro Props 接口
    用于显示不包含内容主体的文章列表
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
    文章创建模型 - 用于创建新文章
    内容字段与元数据分离
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
    更新后模型 - 用于更新现有文章
    所有字段均为可选字段，以允许部分更新
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
    完整的帖子模型 - 包含内容主体
    用于查看和编辑文章详情
    Complete post model - includes content body
    Used for article detail view and editing
    """
    content: str


class PostResponse(BaseModel):
    """
    后期操作的标准 API 响应
    Standard API response for post operations
    """
    success: bool
    message: str
    data: Optional[dict] = None