"""
数据库连接和会话管理
配置 SQLAlchemy 引擎，提供数据库会话依赖项
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from ..core.config import settings

# 创建数据库引擎
# SQLite 不需要连接池，但为了兼容性保留 pool_pre_ping
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite 特有配置
    pool_pre_ping=True,
)

# 创建会话工厂
# autocommit=False: 事务需手动提交
# autoflush=False: 不自动刷新，提高性能
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建模型基类
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    数据库会话依赖项
    FastAPI 依赖注入系统会自动调用此函数，为每个请求提供独立的数据库会话
    使用生成器确保会话在请求结束后正确关闭
    """
    db = SessionLocal()
    try:
        yield db  # 提供数据库会话给路由处理函数
    finally:
        db.close()  # 确保会话总是被关闭，避免连接泄漏


def create_tables():
    """
    创建所有数据库表
    在应用启动时调用，确保数据库表结构是最新的
    """
    Base.metadata.create_all(bind=engine)