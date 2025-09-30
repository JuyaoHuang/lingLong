"""
Authentication API routes
Handles user login and JWT token generation
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..data.database import get_db
from ..services.user_service import authenticate_user
from ..core.security import create_access_token
from ..core.config import settings
from ..schemas.user import Token

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    用户登录接口 - 获取JWT访问令牌
    OAuth2 compatible token login endpoint

    功能说明：
    - 验证管理员用户名和密码
    - 生成JWT访问令牌用于后续API调用认证
    - 这是唯一不需要认证的接口，是获取token的入口

    Args:
        form_data: OAuth2PasswordRequestForm containing username and password
        db: Database session dependency

    Returns:
        JWT access token and token type

    Raises:
        HTTPException: 401 if authentication fails

    Note:
        This endpoint is not protected by JWT - it's the entry point for authentication
        Frontend should POST to this endpoint with username/password to get a token
    """
    # 验证用户凭据 - Authenticate user credentials
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 创建JWT访问令牌 - Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }