#!/bin/bash

# ============================================
# 自动化部署脚本 (双仓库架构)
# 用途：从 GitHub 拉取代码和内容，重新构建前端
# ============================================

set -e  # 遇到错误立即退出

# 配置变量
PROJECT_DIR="$(dirname "$(realpath "$0")")"
LOG_FILE="$PROJECT_DIR/deploy.log"
CODE_BRANCH="dev"           # 代码仓库分支
CONTENT_BRANCH="master"     # 内容仓库分支
CODE_DIR="$PROJECT_DIR/code/lingLong"
CONTENT_DIR="$PROJECT_DIR/contents"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=========================================="
log "开始自动化部署流程"
log "=========================================="

# 1. 拉取内容仓库
log ">>> [1/4] 拉取内容仓库..."
cd "$CONTENT_DIR" || { log "错误：无法进入内容目录 $CONTENT_DIR"; exit 1; }
git fetch origin "$CONTENT_BRANCH"
git reset --hard "origin/$CONTENT_BRANCH"
log "内容仓库更新完成"

# 2. 拉取代码仓库
log ">>> [2/4] 拉取代码仓库..."
cd "$CODE_DIR" || { log "错误：无法进入代码目录 $CODE_DIR"; exit 1; }
git fetch origin "$CODE_BRANCH"
git reset --hard "origin/$CODE_BRANCH"
log "代码仓库更新完成"

# 3. 安装依赖并构建
log ">>> [3/4] 检查并安装依赖..."
pnpm install --frozen-lockfile
log "依赖安装完成"

log "开始构建前端..."
pnpm build
log "前端构建完成"

# 4. 重启 Nginx 容器
cd "$PROJECT_DIR"
log ">>> [4/4] 重启 Nginx 容器..."
docker compose restart nginx
log "Nginx 重启完成"

log "=========================================="
log "部署完成！"
log "=========================================="
