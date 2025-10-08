#!/bin/bash

# ============================================
# Cron 定时任务设置脚本 (双仓库架构)
# 用途：为 deploy.sh 创建定时任务 (每6小时)
# 部署路径：~/blog/
# ============================================

set -e # 遇到错误立即退出

# ==== 配置 ====
# 定义定时任务的执行周期 (使用 Cron 语法)
# 示例：'0 */6 * * *'  => 每 6 小时执行一次 (在 0, 6, 12, 18 点的 0 分)
# 示例：'0 4,16 * * *' => 每天的 4:00 和 16:00 执行
CRON_SCHEDULE="0 */6 * * *"

# ==== 脚本开始 ====
echo ">>> 开始设置自动化部署的 Cron 定时任务..."

# 获取 deploy.sh 脚本的绝对路径
SCRIPT_PATH="$(realpath "$(dirname "$0")/deploy.sh")"
echo ">>> 部署脚本路径: $SCRIPT_PATH"

# 检查 deploy.sh 脚本是否存在且有执行权限
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "!!! 错误：部署脚本 'deploy.sh' 未在期望的路径找到！"
    exit 1
fi
if [ ! -x "$SCRIPT_PATH" ]; then
    echo "!!! 警告：部署脚本 'deploy.sh' 没有执行权限。正在尝试添加..."
    chmod +x "$SCRIPT_PATH"
    echo ">>> 已添加执行权限。"
fi

# 构造完整的 Cron 命令
# 重定向日志输出到 deploy.log
PROJECT_DIR=$(dirname "$SCRIPT_PATH")
CRON_COMMAND="cd $PROJECT_DIR && $SCRIPT_PATH >> $PROJECT_DIR/deploy.log 2>&1"
CRON_JOB="$CRON_SCHEDULE $CRON_COMMAND"

echo ">>> 将要设置的 Cron 任务: $CRON_JOB"

# 检查定时任务是否已经存在，避免重复添加
# (crontab -l || true) 确保在没有任务时命令不会因报错而退出
EXISTING_JOBS=$(crontab -l || true)
if echo "$EXISTING_JOBS" | grep -Fq "$CRON_COMMAND"; then
    echo ">>> 定时任务已经存在，无需重复添加。"
    echo ">>> 当前任务列表:"
    crontab -l
    exit 0
fi

# 如果任务不存在，则添加到 crontab 中
# 我们先移除所有旧的、可能指向此脚本的条目，然后再添加新的，确保唯一性
CLEANED_JOBS=$(echo "$EXISTING_JOBS" | grep -Fv "$SCRIPT_PATH")
(echo "$CLEANED_JOBS"; echo "$CRON_JOB") | crontab -

echo ">>> 成功！新的定时任务已添加到系统中。"
echo ">>> 当前任务列表:"
crontab -l
echo ">>> 设置完成。"