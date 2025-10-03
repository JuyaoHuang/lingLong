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
    # 警告：生产环境必须通过环境变量 SECRET_KEY 设置强密钥
    # 可使用命令生成：python -c "import secrets; print(secrets.token_urlsafe(32))"
    SECRET_KEY: str = "your KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1  # 1天

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

    # CORS 配置 - 允许跨域来源
    # 开发环境：可设置为空使用默认的本地端口
    # 生产环境：必须在 .env 中明确指定域名，如：ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
    ALLOWED_ORIGINS: Optional[str] = None

    # 本地开发端口范围配置
    LOCAL_PORT_RANGE_START: int = 4321
    LOCAL_PORT_RANGE_END: int = 5000

    class Config:
        env_file = ".env"
        case_sensitive = True

# 创建全局设置实例
settings = Settings()

# 处理 ALLOWED_ORIGINS 配置
def get_allowed_origins() -> list[str]:
    """
    获取允许的跨域来源列表

    开发环境：使用本地端口范围
    生产环境：从 .env 读取域名列表（逗号分隔）
    """
    if settings.ALLOWED_ORIGINS:
        # 从环境变量读取，支持逗号分隔的多个域名
        return [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",")]

    # 默认开发环境配置
    return (
        # 基础端口
        ["http://localhost:3000", "http://127.0.0.1:3000"] +
        # 开发端口范围 (localhost)
        [f"http://localhost:{port}" for port in range(settings.LOCAL_PORT_RANGE_START, settings.LOCAL_PORT_RANGE_END + 1)] +
        # 开发端口范围 (127.0.0.1)
        [f"http://127.0.0.1:{port}" for port in range(settings.LOCAL_PORT_RANGE_START, settings.LOCAL_PORT_RANGE_END + 1)]
    )

# 全局 CORS 配置
ALLOWED_ORIGINS = get_allowed_origins()

# 安全检查：生产环境必须使用强密钥
if settings.ENVIRONMENT == "production" and "INSECURE" in settings.SECRET_KEY:
    import sys
    print("\n" + "="*60)
    print("⚠️  严重安全警告 - CRITICAL SECURITY WARNING")
    print("="*60)
    print("检测到生产环境使用了不安全的默认SECRET_KEY！")
    print("Production environment detected with INSECURE default SECRET_KEY!")
    print("\n请立即设置环境变量：")
    print("Please set environment variable immediately:")
    print('  export SECRET_KEY="$(python -c \'import secrets; print(secrets.token_urlsafe(32))\')"')
    print("\n或在 .env 文件中设置：")
    print("Or set in .env file:")
    print("  SECRET_KEY=<your-strong-random-key>")
    print("="*60 + "\n")
    sys.exit(1)

# 确保关键目录存在
def ensure_directories():
    """确保必要的目录存在"""
    astro_content_path = Path(settings.ASTRO_CONTENT_PATH)
    database_dir = Path("./data")

    astro_content_path.mkdir(parents=True, exist_ok=True)
    database_dir.mkdir(parents=True, exist_ok=True)


# 初始化时调用
ensure_directories()