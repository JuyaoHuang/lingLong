# 集成部署用的完整版 Dockerfile
# 用途：在根目录使用，构建上下文是项目根目录，可以访问整个项目文件

FROM python:3.11-slim-bookworm

USER root

# 安装必要的系统依赖（包括 gosu 用于权限切换）
RUN apt-get update && apt-get install -y curl git gosu && rm -rf /var/lib/apt/lists/*

# 安装 Node.js----后端运行pnpm build脚本需要
ENV NODE_VERSION=22
RUN curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION}.x | bash - \
    && apt-get install -y nodejs

# 配置 npm 镜像源并安装 pnpm
RUN npm config set registry https://registry.npmmirror.com && npm install -g pnpm

# 配置 pnpm 镜像源
RUN pnpm config set registry https://registry.npmmirror.com

# 设置工作目录
WORKDIR /code

# 配置 PIP 清华源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 复制并安装 Python 依赖
COPY backend/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 复制后端代码
COPY backend/app /code/app

# 创建前端项目目录并复制依赖文件
RUN mkdir -p /code/lingLong
COPY lingLong/package.json /code/lingLong/package.json
COPY lingLong/pnpm-lock.yaml /code/lingLong/pnpm-lock.yaml

# 在构建时安装前端依赖
RUN cd /code/lingLong && pnpm install --frozen-lockfile

# 创建非root用户运行应用
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /code

# 复制启动脚本
COPY backend/docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# 注意：不在这里切换USER，而是在entrypoint中切换

# 暴露端口
EXPOSE 8000

# 使用启动脚本作为入口点
ENTRYPOINT ["docker-entrypoint.sh"]

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
