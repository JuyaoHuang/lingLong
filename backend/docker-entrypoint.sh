#!/bin/bash
# Docker 容器启动脚本 - Docker container entrypoint script
# 用途：修复卷挂载后的权限问题 - Fix permission issues after volume mounting

set -e

echo "=== Starting Backend Container ==="

# 修复 dist 目录权限（如果存在）- Fix dist directory permissions if exists
if [ -d "/code/lingLong/dist" ]; then
    echo "Fixing /code/lingLong/dist permissions..."
    # 注意：这里以 root 运行，然后切换到 appuser
    chown -R appuser:appuser /code/lingLong/dist
    chmod -R 755 /code/lingLong/dist
    echo "✓ dist permissions fixed"
fi

# 修复 node_modules 权限（如果存在）- Fix node_modules permissions if exists
if [ -d "/code/lingLong/node_modules" ]; then
    echo "Fixing /code/lingLong/node_modules permissions..."
    chown -R appuser:appuser /code/lingLong/node_modules
    echo "✓ node_modules permissions fixed"
fi

# 切换到 appuser 并执行传入的命令 - Switch to appuser and execute command
echo "Switching to appuser and starting application..."
exec gosu appuser "$@"
