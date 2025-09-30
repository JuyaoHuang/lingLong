"""
FastAPI 应用核心配置
使用 Pydantic Settings 管理所有环境变量和配置
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用程序设置配置类"""

    # JWT 配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天

    # 数据库配置
    DATABASE_URL: str = "sqlite:///./data/dataBase.db"

    # Astro 项目配置 - Docker容器内的路径
    ASTRO_CONTENT_PATH: str = "/code/yukina/src/contents/posts"
    ASTRO_PROJECT_PATH: str = "/code/yukina"

    # API 配置
    API_PREFIX: str = "/api"
    PROJECT_NAME: str = "Blog Backend API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "博客管理后端API"

    # 环境配置
    ENVIRONMENT: str = "production"  # development | production

    # CORS 配置 - 允许4321-5000端口范围的跨域访问
    ALLOWED_ORIGINS: list[str] = (
        # 基础端口
        ["http://localhost:3000", "http://127.0.0.1:3000"] +
        # 开发端口范围 4321-5000 (localhost)
        [f"http://localhost:{port}" for port in range(4321, 5001)] +
        # 开发端口范围 4321-5000 (127.0.0.1)
        [f"http://127.0.0.1:{port}" for port in range(4321, 5001)]
    )

    class Config:
        env_file = ".env"
        case_sensitive = True
# eeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc1OTY3OTcwOX0.xVnPwsr9erVRaBX0WWNszyAptZEPhWWMYBANOP2dq6E

# 创建全局设置实例
settings = Settings()

# 确保关键目录存在
def ensure_directories():
    """确保必要的目录存在"""
    astro_content_path = Path(settings.ASTRO_CONTENT_PATH)
    database_dir = Path("./data")

    astro_content_path.mkdir(parents=True, exist_ok=True)
    database_dir.mkdir(parents=True, exist_ok=True)


# 初始化时调用
ensure_directories()