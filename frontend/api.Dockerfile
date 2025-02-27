# 使用 Python 3.9-slim 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 到容器的工作目录
COPY requirements.txt /app/

# 安装依赖项
RUN pip install -r requirements.txt

# 复制整个 frontend 目录到容器的工作目录
COPY . /app/


# 设置 Flask 启动命令，确保环境变量设置正确
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=52005

# 暴露 Flask 服务端口
EXPOSE 52005

# 设置容器启动时执行的命令
CMD ["flask", "run"]

