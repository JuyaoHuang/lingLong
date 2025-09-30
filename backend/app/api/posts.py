"""
Posts management API routes
Handles all CRUD operations for blog articles
All endpoints require JWT authentication
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..data.database import get_db
from ..data.models import User
from ..core.security import get_current_user
from ..services import post_service
from ..schemas.post import PostMetadata, PostCreate, PostUpdate, PostFull, PostResponse

router = APIRouter()


@router.get("/posts", response_model=List[PostMetadata])
async def get_all_posts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取所有文章元数据列表 - Get all posts metadata (without content body)

    功能说明：
    - 返回所有文章的元数据（不包含文章内容主体）
    - 按发布日期排序，用于管理面板文章列表显示
    - 需要JWT认证的受保护接口

    Returns:
        List of all posts with metadata only, sorted by publication date

    Note:
        Protected endpoint - requires valid JWT token
        Used for admin dashboard article list display
    """
    try:
        posts_metadata = post_service.get_all_posts_metadata()
        return posts_metadata
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch posts: {str(e)}"
        )


@router.get("/posts/{slug}", response_model=PostFull)
async def get_post_by_slug(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    根据Slug获取完整文章数据 - Get complete post data by slug

    功能说明：
    - 根据文章的slug标识符获取完整文章数据
    - 包含文章内容主体，用于文章编辑界面
    - 需要JWT认证的受保护接口

    Args:
        slug: Post identifier (filename without extension)

    Returns:
        Complete post data including content body

    Raises:
        HTTPException: 404 if post not found

    Note:
        Protected endpoint - requires valid JWT token
        Used for post editing interface
    """
    post = post_service.get_post_by_slug(slug)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with slug '{slug}' not found"
        )

    return post


@router.post("/posts", response_model=PostResponse)
async def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    创建新文章 - Create new post

    功能说明：
    - 创建新的博客文章
    - 自动生成slug标识符
    - 创建后自动触发Astro项目重新构建
    - 需要JWT认证的受保护接口

    Args:
        post_data: Complete post data including content

    Returns:
        Success/failure response with details

    Note:
        Protected endpoint - requires valid JWT token
        Automatically triggers Astro project rebuild after creation
    """
    try:
        # 将Pydantic模型转换为字典供服务层使用 - Convert Pydantic model to dict for service layer
        post_dict = post_data.dict()

        success = post_service.create_post(post_dict)

        if success:
            return PostResponse(
                success=True,
                message="Post created successfully",
                data={"slug": post_service._generate_slug(post_data.title)}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create post"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create post: {str(e)}"
        )


@router.put("/posts/{slug}", response_model=PostResponse)
async def update_post(
    slug: str,
    post_data: PostUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新现有文章 - Update existing post

    功能说明：
    - 更新指定文章的内容（支持部分更新）
    - 更新后自动触发Astro项目重新构建
    - 需要JWT认证的受保护接口

    Args:
        slug: Post identifier
        post_data: Updated post data (partial updates allowed)

    Returns:
        Success/failure response with details

    Raises:
        HTTPException: 404 if post not found

    Note:
        Protected endpoint - requires valid JWT token
        Automatically triggers Astro project rebuild after update
    """
    try:
        # Check if post exists
        existing_post = post_service.get_post_by_slug(slug)
        if not existing_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with slug '{slug}' not found"
            )

        # Convert Pydantic model to dict, excluding None values for partial updates
        post_dict = post_data.dict(exclude_unset=True)

        # If no fields to update
        if not post_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update"
            )

        # Merge with existing data for partial updates
        updated_data = {**existing_post, **post_dict}

        success = post_service.update_post(slug, updated_data)

        if success:
            return PostResponse(
                success=True,
                message="Post updated successfully",
                data={"slug": slug}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to update post"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update post: {str(e)}"
        )


@router.delete("/posts/{slug}", response_model=PostResponse)
async def delete_post(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    删除文章 - Delete post

    功能说明：
    - 删除指定的文章文件
    - 删除后自动触发Astro项目重新构建
    - 该操作不可逆转，请谨慎操作
    - 需要JWT认证的受保护接口

    Args:
        slug: Post identifier

    Returns:
        Success/failure response with details

    Raises:
        HTTPException: 404 if post not found

    Note:
        Protected endpoint - requires valid JWT token
        Automatically triggers Astro project rebuild after deletion
        This operation is irreversible
    """
    try:
        # Check if post exists
        existing_post = post_service.get_post_by_slug(slug)
        if not existing_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with slug '{slug}' not found"
            )

        success = post_service.delete_post(slug)

        if success:
            return PostResponse(
                success=True,
                message="Post deleted successfully",
                data={"slug": slug}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to delete post"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete post: {str(e)}"
        )