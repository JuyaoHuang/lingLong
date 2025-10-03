"""
数据库连接和会话管理
配置 SQLAlchemy 引擎，提供数据库会话依赖项
Database connection and session management 
Configure the SQLAlchemy engine and provide database session dependencies
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from ..core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite-specific configuration
    pool_pre_ping=True,
)

# 创建会话工厂
# autocommit=False: 事务需手动提交
# autoflush=False: 不自动刷新，提高性能
# autocommit=False: Transactions must be manually committed
# autoflush=False: Disable automatic flushing to improve performance
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    数据库会话依赖项
    FastAPI 依赖注入系统会自动调用此函数，为每个请求提供独立的数据库会话
    使用生成器确保会话在请求结束后正确关闭
    Database Session Dependency
    The FastAPI dependency injection system automatically calls this function to provide a separate database session for each request.
    Use a generator to ensure that the session is properly closed after the request ends.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  


def create_tables():
    """
    创建所有数据库表
    在应用启动时调用，确保数据库表结构是最新的
    Create all database tables. 
    Called when the application starts to ensure that the database table structure is up to date.
    """
    Base.metadata.create_all(bind=engine)