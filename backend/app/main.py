"""
FastAPI博客后端应用程序 - FastAPI Blog Backend Application
主应用程序入口点，包含路由配置和中间件设置 - Main application entry point with route configuration and middleware setup
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .core.config import settings, ALLOWED_ORIGINS
from .data.database import create_tables
from .api import auth, posts

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用程序生命周期管理 - Application lifespan management

    启动时：创建数据库表
    关闭时：清理资源（如需要）

    Startup: Create database tables
    Shutdown: Cleanup resources (if needed)
    """
    # 启动时执行 - Execute on startup
    create_tables()
    print("Database tables created/verified")
    print(f"API Documentation available at: http://localhost:8000/docs")
    print(f"Authentication endpoint: POST /token")
    print(f"Admin posts endpoint: {settings.API_PREFIX}/admin/posts")

    yield  # 应用程序运行期间 - Application running

    print("Shutting down...")


# 创建FastAPI应用程序实例 - Create FastAPI application instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs",  # Swagger UI文档 - Swagger UI documentation
    redoc_url="/redoc",  # ReDoc文档 - ReDoc documentation
    lifespan=lifespan  # 使用生命周期管理器 - Use lifespan manager
)

# 配置CORS中间件 - Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# 包含API路由器 - Include API routers
app.include_router(auth.router, tags=["Authentication"])
app.include_router(
    posts.router,
    prefix=settings.API_PREFIX + "/admin",
    tags=["Posts Management"]
)

# 健康检查端点 - Health check endpoint
@app.get("/")
async def root():
    """
    健康检查端点 - Health check endpoint

    功能说明：
    - 返回基本的应用程序状态信息
    - 用于确认API服务是否正常运行
    - 可用于负载均衡器的健康检查

    Returns basic application status
    """
    return {
        "message": "Blog Backend API is running!",
        "version": settings.VERSION,
        "project": settings.PROJECT_NAME
    }