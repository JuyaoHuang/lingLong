#!/bin/bash

# ============================================
# 自动化部署脚本
# 用途：从 GitHub 拉取最新代码并重新构建前端
# ============================================

set -e  # 遇到错误立即退出

# 配置变量
PROJECT_DIR="$(dirname "$(realpath "$0")")"
LOG_FILE="$PROJECT_DIR/deploy.log"
BRANCH="master"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=========================================="
log "开始自动化部署流程"
log "=========================================="

# 进入项目目录
cd "$PROJECT_DIR" || { log "错误：无法进入项目目录 $PROJECT_DIR"; exit 1; }
log "当前目录: $(pwd)"

# 拉取最新代码
log "正在从 GitHub 拉取最新代码..."
git fetch origin "$BRANCH"
git reset --hard "origin/$BRANCH"
log "代码拉取完成"

# 进入前端目录
cd lingLong || { log "错误：无法进入 lingLong 目录"; exit 1; }

# 安装依赖（如果 package.json 有更新）
log "检查并安装依赖..."
pnpm install --frozen-lockfile
log "依赖安装完成"

# 构建前端
log "开始构建前端..."
pnpm build
log "前端构建完成"

# 重启 Nginx 容器以加载新的静态文件
cd "$PROJECT_DIR"
log "重启 Nginx 容器..."
docker compose restart nginx
log "Nginx 重启完成"

log "=========================================="
log "部署完成！"
log "=========================================="
