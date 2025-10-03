# 选择一个官方的、支持多平台架构的 Python 基础镜像
#   python:3.11-slim-bookworm 是一个很好的选择，它同时有 amd64(PC) 和 arm64(Pi) 版本
# Choose an official, multi-platform Python base image
# python:3.11-slim-bookworm is a good choice; it has both amd64 (PC) and arm64 (Pi) versions.
FROM python:3.11-slim-bookworm

# 设置容器内的工作目录--Set the working directory in the container
WORKDIR /code

# 设置 PIP 清华源以加速--Set up PIP Tsinghua source to accelerate(In China)
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 复制依赖文件并安装依赖
#  将这一步分开是为了利用 Docker 的层缓存机制，只要 requirements.txt 不变，就不需要重新安装
# Copy the dependency files and install them
# This step is separated to take advantage of Docker's layer caching mechanism. 
# As long as requirements.txt remains unchanged, there is no need to reinstall.
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 复制所有应用源代码到工作目录
# Copy all application source code to the working directory
COPY ./app /code/app

# 暴露 FastAPI 应用运行的端口
# Expose the port where the FastAPI application is running
EXPOSE 8000

# 定义容器启动时要执行的命令
# Defines the command to be executed when the container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]