"""
初始化管理员用户
在应用启动时自动创建或更新管理员账户
Initialize admin user
Automatically create or update admin account on application startup
"""
from sqlalchemy.orm import Session
from ..data.models import User
from ..data.database import SessionLocal
from .security import get_password_hash
from .config import settings
import logging

logger = logging.getLogger(__name__)


def init_admin_user() -> None:
    """
    初始化管理员用户
    - 如果管理员不存在，则创建
    - 如果存在但密码已更改，则更新密码
    
    Initialize admin user
    - Create if admin doesn't exist
    - Update password if exists and password changed
    """
    if not settings.ADMIN_PASSWORD:
        logger.warning(
            "⚠️  ADMIN_PASSWORD not set in environment variables. "
            "Please set PASSWORD in .env file to initialize admin user."
        )
        return

    db: Session = SessionLocal()
    try:
        # 查找管理员用户
        admin_user = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()

        if not admin_user:
            logger.info(f"Creating admin user: {settings.ADMIN_USERNAME}")
            hashed_password = get_password_hash(settings.ADMIN_PASSWORD)
            admin_user = User(
                username=settings.ADMIN_USERNAME,
                hashed_password=hashed_password
            )
            db.add(admin_user)
            db.commit()
            logger.info(f"✅ Admin user '{settings.ADMIN_USERNAME}' created successfully")
        else:
            # 更新现有管理员密码（如果 .env 中的密码已更改）
            logger.info(f"Admin user '{settings.ADMIN_USERNAME}' already exists")
            new_hashed_password = get_password_hash(settings.ADMIN_PASSWORD)
            
            # 只有密码哈希不同时才更新
            if admin_user.hashed_password != new_hashed_password:
                admin_user.hashed_password = new_hashed_password
                db.commit()
                logger.info(f"✅ Admin user '{settings.ADMIN_USERNAME}' password updated")
            else:
                logger.info(f"✅ Admin user '{settings.ADMIN_USERNAME}' password unchanged")

    except Exception as e:
        logger.error(f"❌ Error initializing admin user: {e}")
        db.rollback()
        raise
    finally:
        db.close()
