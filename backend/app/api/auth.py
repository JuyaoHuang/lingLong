"""
Authentication API routes
Handles user login and JWT token generation with rate limiting
"""
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..data.database import get_db
from ..services.user_service import authenticate_user
from ..core.security import create_access_token
from ..core.config import settings
from ..core.rate_limiter import rate_limiter
from ..schemas.user import Token

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    用户登录接口 - 获取JWT访问令牌（带速率限制）
    OAuth2 compatible token login endpoint with rate limiting

    功能说明：
    - 验证管理员用户名和密码
    - 生成JWT访问令牌用于后续API调用认证
    - 速率限制：5次失败后锁定30分钟
    - 这是唯一不需要认证的接口，是获取token的入口

    Args:
        form_data: OAuth2PasswordRequestForm containing username and password
        db: Database session dependency

    Returns:
        JWT access token and token type

    Raises:
        HTTPException: 401 if authentication fails
        HTTPException: 429 if rate limit exceeded (too many failed attempts)

    Note:
        This endpoint is not protected by JWT - it's the entry point for authentication
        Frontend should POST to this endpoint with username/password to get a token
    """
    username = form_data.username

    # 检查账户是否被锁定 - Check if account is locked
    if rate_limiter.is_locked(username):
        lockout_time = rate_limiter.get_lockout_time(username)
        remaining_minutes = int((lockout_time - datetime.now()).total_seconds() / 60)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Account locked due to too many failed login attempts. Please try again in {remaining_minutes} minutes.",
            headers={"Retry-After": str(remaining_minutes * 60)},
        )

    # 验证用户凭据 - Authenticate user credentials
    user = authenticate_user(db, username, form_data.password)

    if not user:
        # 记录失败尝试 - Record failed attempt
        rate_limiter.record_failed_attempt(username)
        remaining = rate_limiter.get_remaining_attempts(username)

        if remaining > 0:
            detail = f"Incorrect username or password. {remaining} attempts remaining."
        else:
            detail = "Account locked due to too many failed login attempts. Please try again in 30 minutes."

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 登录成功，重置失败计数 - Successful login, reset counter
    rate_limiter.record_successful_login(username)

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