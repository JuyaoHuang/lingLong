"""
用户认证业务逻辑服务 - User authentication business logic service
处理用户登录验证和用户管理核心业务逻辑 - Handles user login verification and user management core business logic
"""
from sqlalchemy.orm import Session
from typing import Optional

from ..data.models import User
from ..core.security import verify_password


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    验证用户登录凭据 - Verify user credentials

    功能说明：
    - 验证用户名和密码的正确性
    - 用于用户登录流程，是JWT令牌生成的前置步骤
    - 使用bcrypt进行密码哈希验证

    Args:
        db: Database session
        username: Username
        password: Plain text password

    Returns:
        Returns User object if verification successful, None if failed

    Process:
        1. Find user from database by username
        2. If user exists, verify password hash
        3. Return user object if password correct, otherwise return None
    """
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return None

    # 验证密码（将明文密码与数据库中的哈希密码比较） - Verify password (compare plain text password with hashed password in database)
    if not verify_password(password, user.hashed_password):
        return None

    return user


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    根据用户名获取用户信息 - Get user information by username

    功能说明：
    - 从数据库中根据用户名查找用户记录
    - 用于用户查询和验证功能

    Args:
        db: Database session
        username: Username

    Returns:
        Returns User object if found, otherwise None
    """
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    根据用户ID获取用户信息 - Get user information by user ID

    功能说明：
    - 从数据库中根据用户ID查找用户记录
    - 用于JWT令牌解析后的用户信息获取

    Args:
        db: Database session
        user_id: User ID

    Returns:
        Returns User object if found, otherwise None
    """
    return db.query(User).filter(User.id == user_id).first()