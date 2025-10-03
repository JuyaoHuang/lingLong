# lingLong Blog - Full-Stack Integrated Project

> **简洁优雅的 Astro 博客系统 + FastAPI 后端管理平台**
> A simple and elegant Astro blog system with FastAPI backend management platform

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Astro](https://img.shields.io/badge/Astro-5.3-orange.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-green.svg)
![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)

---

## 📋 项目简介 | Project Overview

本项目是一个**前后端集成的博客系统**，结合了现代化的静态网站生成技术和强大的后端管理能力：

- **前端 (LingLong)**: 基于 Astro 5 的静态博客，支持 Markdown、数学公式、搜索、RSS 等功能
- **后端 (FastAPI)**: 提供博客内容管理 API，支持文章的创建、编辑、删除和身份验证
- **部署方案**: Docker + Nginx 反向代理，适合树莓派/VPS 部署

---

## ✨ 核心特性 | Key Features

### 🎨 前端特性

- ✅ **现代化设计**: 简洁优雅的 UI，支持深色模式
- ✅ **Markdown 增强**: 支持 KaTeX 数学公式、代码高亮、自动目录
- ✅ **全文搜索**: 基于 Pagefind 的快速客户端搜索
- ✅ **分类系统**: 支持多级分类和标签管理
- ✅ **SEO 优化**: 自动生成 Sitemap、RSS 和元数据
- ✅ **国际化**: 内置中英文支持
- ✅ **性能优化**: 静态生成 + 图片懒加载 + 平滑过渡动画

### 🔧 后端特性

- ✅ **RESTful API**: 完整的文章管理接口
- ✅ **JWT 认证**: 安全的身份验证系统
- ✅ **Markdown 处理**: 自动解析和管理 Markdown 文件
- ✅ **SQLite 数据库**: 轻量级用户管理
- ✅ **Swagger 文档**: 自动生成的 API 文档
- ✅ **CORS 配置**: 灵活的跨域访问控制

### 🚀 部署特性

- ✅ **Docker 化**: 一键部署，环境隔离
- ✅ **Nginx 反向代理**: 前后端统一入口，无需 CORS 配置
- ✅ **开发/生产分离**: 独立的开发和部署环境
- ✅ **树莓派友好**: 针对 ARM 架构优化

---

## 🏗️ 技术栈 | Tech Stack

### 前端 Frontend

| 技术 | 版本 | 用途 |
|------|------|------|
| **Astro** | 5.3.0 | 静态站点生成器 |
| **Svelte** | 5.39.6 | 交互式组件 (搜索栏、管理面板) |
| **Tailwind CSS** | 3.4.17 | 样式框架 |
| **Pagefind** | 1.3.0 | 全文搜索引擎 |
| **TypeScript** | 5.9.2 | 类型安全 |

### 后端 Backend

| 技术 | 用途 |
|------|------|
| **FastAPI** | Web 框架 |
| **SQLAlchemy** | ORM 数据库管理 |
| **SQLite** | 数据存储 |
| **JWT (python-jose)** | 身份认证 |
| **Passlib + Bcrypt** | 密码加密 |
| **Python Frontmatter** | Markdown 解析 |

### 基础设施 Infrastructure

| 技术 | 用途 |
|------|------|
| **Docker** | 容器化部署 |
| **Nginx** | 反向代理 + 静态文件服务 |
| **pnpm** | 前端包管理 |

---

## 📦 项目结构 | Project Structure

```
webTest/
├── lingLong/                    # 前端项目 (Astro)
│   ├── src/
│   │   ├── components/        # UI 组件
│   │   ├── contents/posts/    # Markdown 文章
│   │   ├── layouts/           # 页面布局
│   │   ├── pages/             # 路由页面
│   │   ├── utils/             # 工具函数
│   │   └── styles/            # 样式文件
│   ├── public/                # 静态资源
│   ├── dist/                  # 构建产物
│   └── package.json
│
├── backend/                   # 后端项目 (FastAPI)
│   ├── app/
│   │   ├── api/               # API 路由
│   │   │   ├── auth.py        # 认证接口
│   │   │   └── posts.py       # 文章管理接口
│   │   ├── core/              # 核心配置
│   │   │   ├── config.py      # 环境变量配置
│   │   │   └── security.py    # 安全认证逻辑
│   │   ├── data/              # 数据层
│   │   │   ├── database.py    # 数据库连接
│   │   │   └── models.py      # 数据模型
│   │   └── main.py            # 应用入口
│   ├── data/                  # SQLite 数据库文件
│   ├── .env                   # 环境变量 (不提交到 Git)
│   ├── .env.example           # 环境变量示例
│   ├── Dockerfile             # 后端独立开发用
│   └── requirements.txt
│
├── nginx/                     # Nginx 配置
│   ├── nginx.conf             # 反向代理配置
│   └── Dockerfile
│
├── backend.Dockerfile         # 后端集成部署用
├── docker-compose.yml         # 集成部署配置
└── README.md                  # 本文件
```

---

## 🚀 快速开始 | Quick Start

### 📋 前置要求 | Prerequisites

- **Node.js** >= 22.0
- **Python** >= 3.11
- **Docker** >= 20.10
- **Docker Compose** >= 2.0
- **pnpm** (通过 Corepack 启用)

---

## 🛠️ 开发模式 | Development Mode

### 1️⃣ 前端开发

```bash
# 进入前端目录
cd lingLong

# 启用 Corepack (首次)
corepack enable

# 安装依赖
pnpm install

# 启动开发服务器 (http://localhost:4321)
pnpm dev

# 构建生产版本
pnpm build

# 预览构建结果
pnpm preview
```

### 2️⃣ 后端开发

```bash
# 进入后端目录
cd backend

# 创建虚拟环境 (可选)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置 SECRET_KEY

# 启动开发服务器 (http://localhost:8000)
uvicorn app.main:app --reload

# 访问 API 文档
# http://localhost:8000/docs
```

### 3️⃣ Docker 独立后端开发

```bash
cd backend
docker-compose up --build
```

---

## 🐳 生产部署 | Production Deployment

### 方式一：Docker Compose (推荐)

```bash
# 1. 配置环境变量
cd backend
cp .env.example .env
# 编辑 .env，设置生产环境配置：
#   - SECRET_KEY: 强密钥 (使用 python -c "import secrets; print(secrets.token_urlsafe(32))")
#   - ALLOWED_ORIGINS: 留空 (Nginx 反向代理模式)
#   - ENVIRONMENT: production

# 2. 构建前端
cd ../lingLong
pnpm install
pnpm build

# 3. 启动集成服务 (在项目根目录)
cd ..
docker-compose up -d

# 4. 访问服务
# 前端: http://localhost:8080
# 后端 API: http://localhost:8080/api
# API 文档: http://localhost:8080/docs
```

### 方式二：树莓派 + Cloudflare 部署

#### 1. 树莓派配置

```bash
# 克隆项目
git clone <your-repo-url> ~/webTest
cd ~/webTest

# 配置后端环境
cd backend
cp .env.example .env
nano .env  # 配置生产环境变量

# 构建前端
cd ../lingLong
pnpm install
pnpm build

# 启动服务
cd ..
docker-compose up -d

# 配置防火墙 (可选)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

#### 2. Cloudflare 配置

**DNS 设置**:
- 类型: `A`
- 名称: `@` (或子域名)
- 内容: `树莓派公网 IP`
- 代理状态: `已代理` (橙色云朵)

**SSL/TLS 设置**:
- 模式: `灵活` 或 `完全`

**访问**:
```
https://yourdomain.com        # 博客首页
https://yourdomain.com/api    # 后端 API
https://yourdomain.com/docs   # API 文档
```

---

## 🔐 环境变量配置 | Environment Configuration

### `backend/.env`

```bash
# ============================================
# JWT 安全配置
# ============================================
# 生成强密钥:
# python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=your-secret-key-here

# ============================================
# CORS 跨域配置
# ============================================
# 开发环境: 留空使用默认本地端口 (localhost:4321-5000)
# 生产环境: 使用 Nginx 反向代理时留空
# 仅在直接暴露不同端口时填写，如:
# ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
ALLOWED_ORIGINS=

# ============================================
# 环境配置
# ============================================
ENVIRONMENT=production  # development | production
```

---

## 📡 API 文档 | API Documentation

### 认证接口

```http
POST /token
Content-Type: application/x-www-form-urlencoded

username=admin&password=your-password

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### 文章管理接口

所有接口需要在 Header 中携带 JWT Token:
```
Authorization: Bearer <token>
```

| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/api/admin/posts` | 获取所有文章列表 |
| POST | `/api/admin/posts` | 创建新文章 |
| PUT | `/api/admin/posts/{slug}` | 更新文章 |
| DELETE | `/api/admin/posts/{slug}` | 删除文章 |

**完整文档**: 部署后访问 `http://your-domain/docs`

---

## 🎯 使用场景 | Use Cases

### ✍️ 日常写作流程

1. 在 `lingLong/src/contents/posts/` 目录创建 Markdown 文件
2. 使用后端 API 管理文章 (可选)
3. 执行 `pnpm build` 重新构建
4. 刷新网站查看更新

### 🔄 自动化部署 (建议)

```bash
# 创建部署脚本 deploy.sh
#!/bin/bash
cd ~/webTest/lingLong
git pull
pnpm install
pnpm build
cd ..
docker-compose restart nginx
```

---

## 🐛 故障排查 | Troubleshooting

### 前端构建失败

```bash
# 清除缓存重新构建
cd lingLong
rm -rf node_modules dist .astro
pnpm install
pnpm build
```

### 后端启动失败

```bash
# 检查日志
docker-compose logs backend

# 常见问题:
# 1. SECRET_KEY 未设置 → 编辑 backend/.env
# 2. 端口占用 → 修改 docker-compose.yml 端口映射
# 3. 数据库权限 → 检查 backend/data/ 目录权限
```

### CORS 错误

```bash
# 确认使用 Nginx 反向代理时:
# 1. backend/.env 中 ALLOWED_ORIGINS 留空
# 2. 通过同一域名访问前后端 (如 yourdomain.com 和 yourdomain.com/api)
```

---

## 📚 更多资源 | Resources

- [Astro 官方文档](https://docs.astro.build/)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Docker 部署指南](https://docs.docker.com/)
- [Nginx 配置参考](https://nginx.org/en/docs/)

---

## 🙏 致谢 | Acknowledgments

### 前端模板基于:
- [Yukina Template by WhitePaper233](https://github.com/WhitePaper233/yukina)
- [Astro Fuwari Template](https://github.com/saicaca/fuwari)
- [Hexo Shoka Theme](https://github.com/amehime/hexo-theme-shoka)

### 技术支持:
- Astro Team
- FastAPI Team
- Docker Community

---

## 📄 许可证 | License

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 👨‍💻 贡献 | Contributing

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📧 联系方式 | Contact

如有问题或建议，请通过以下方式联系:

- 提交 [Issue](https://github.com/JuyaoHuang/lingLong/issues)
- 邮件: your-email@example.com

---

**⭐ 如果这个项目对你有帮助，请给一个 Star 支持！**
