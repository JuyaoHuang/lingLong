"""
SQLAlchemy 数据模型定义
定义应用中使用的所有数据库表结构
"""
from sqlalchemy import Column, Integer, String
from .database import Base


class User(Base):
    """
    用户模型 - 管理员用户表
    对应数据库中的 users 表，用于存储管理员登录信息
    """
    __tablename__ = "users"

    # 主键，自增ID
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # 用户名，唯一且不能为空
    username = Column(String, unique=True, index=True, nullable=False)

    # 哈希后的密码，不能为空
    # 注意：这里存储的是经过 bcrypt 哈希处理的密码，而非明文密码
    hashed_password = Column(String, nullable=False)

    def __repr__(self):
        """字符串表示，方便调试"""
        return f"<User(id={self.id}, username='{self.username}')>"