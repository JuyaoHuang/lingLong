# 1. 选择一个官方的、支持多平台架构的 Python 基础镜像
#    python:3.11-slim-bookworm 是一个很好的选择，它同时有 amd64(PC) 和 arm64(Pi) 版本
FROM python:3.11-slim-bookworm

# 2. 设置容器内的工作目录
WORKDIR /code

# 3. 设置 PIP 清华源以加速（可选，但在国内非常推荐）
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 4. 复制依赖文件并安装依赖
#    将这一步分开是为了利用 Docker 的层缓存机制，只要 requirements.txt 不变，就不需要重新安装
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. 复制你所有的应用源代码到工作目录
COPY ./app /code/app

# 6. 暴露 FastAPI 应用运行的端口 (通常是 8000)
EXPOSE 8000

# 7. 定义容器启动时要执行的命令
#    使用 uvicorn 启动应用。--host 0.0.0.0 使其可以从外部访问。
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]