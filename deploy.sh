# ============================================
# 自动化部署脚本 (双仓库架构)
# 用途：从 GitHub 拉取代码和内容，重新构建前端
# ============================================

set -e  # 遇到错误立即退出

# 加载环境变量
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
ENV_FILE="$SCRIPT_DIR/.env"

if [ -f "$ENV_FILE" ]; then
    # 导出 .env 中的变量
    set -a
    source "$ENV_FILE"
    set +a
    echo "✓ 已加载环境配置: $ENV_FILE"
else
    echo "⚠ 警告：未找到 .env 文件，使用默认配置"
fi

# 配置变量 (优先使用环境变量，否则使用默认值)
PROJECT_DIR="${PROJECT_DIR:-$(dirname "$(realpath "$0")")}"
LOG_FILE="$PROJECT_DIR/deploy.log"
CODE_BRANCH="${CODE_BRANCH:-dev}"              # 代码仓库分支
CONTENT_BRANCH="${CONTENT_BRANCH:-master}"     # 内容仓库分支
CODE_DIR="${CODE_DIR:-$PROJECT_DIR/code/lingLong}"
CONTENT_DIR="${CONTENT_DIR:-$PROJECT_DIR/post}"
PACKAGE_MANAGER="${PACKAGE_MANAGER:-pnpm}"
DOCKER_COMPOSE_CMD="${DOCKER_COMPOSE_CMD:-docker compose}"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=========================================="
log "开始自动化部署流程"
log "=========================================="

# 1. 拉取内容仓库
log ">>> [1/7] 拉取内容仓库..."
cd "$CONTENT_DIR" || { log "错误：无法进入内容目录 $CONTENT_DIR"; exit 1; }
git fetch origin "$CONTENT_BRANCH"
git reset --hard "origin/$CONTENT_BRANCH"
log "内容仓库更新完成"

# 2. 拉取代码仓库
log ">>> [2/7] 拉取代码仓库..."
cd "$CODE_DIR" || { log "错误：无法进入代码目录 $CODE_DIR"; exit 1; }
# git fetch origin "$CODE_BRANCH"
# git reset --hard "origin/$CODE_BRANCH"
log "代码仓库更新完成"

log ">>> [3/7]开始清理dist缓存..."
rm -rf dist
rm -rf node_modules/.vite # Vite的缓存目录
# 为了最彻底的干净，我们也可以直接删掉整个 node_modules
# rm -rf node_modules
log ">>> 缓存清理完成"

log ">>> [4/7] 开始复制文章..."
rm -rf "$CODE_DIR/src/contents/posts"
cp -r "$CONTENT_DIR" "$CODE_DIR/src/contents/posts" || { echo "!!! ERROR: Failed to copy posts"; exit 1; }
log "文章复制完毕: $CONTENT_DIR -> $CODE_DIR/src/contents/posts"

# 3. 安装依赖并构建
log ">>> [5/7] 检查并安装依赖..."
$PACKAGE_MANAGER install --frozen-lockfile
log "依赖安装完成"

log ">>> [6/7] 开始构建前端..."
$PACKAGE_MANAGER build
log "前端构建完成"

# 4. 重启 Nginx 容器
log ">>> [7/7] 更新 Nginx 容器..."
cd "$PROJECT_DIR/code" || { log "错误：无法进入 code 目录"; exit 1; }
log "已进入 code 目录"
# 检查容器是否存在
# if [ -n "$($DOCKER_COMPOSE_CMD ps -q nginx 2>/dev/null)" ]; then
#     log "容器已存在，执行重启..."
#     $DOCKER_COMPOSE_CMD restart nginx
# else
#     log "容器不存在，创建并启动..."
#     $DOCKER_COMPOSE_CMD up -d nginx
# fi
# --force-recreate: 强制重新创建容器，确保挂载的 dist 目录被重新加载
$DOCKER_COMPOSE_CMD up -d --build --force-recreate nginx  || { log "错误: Nginx 部署失败"; exit 1; }
log "Nginx 容器已就绪"

log "=========================================="
log "部署完成！"
log "=========================================="