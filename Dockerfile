FROM python:3.12-slim

WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=Asia/Shanghai

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 创建必要的目录
RUN mkdir -p /app/logs /app/media /app/staticfiles

# 安装Python依赖
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目文件
COPY . .

# 设置权限
RUN chmod +x /app/docker-entrypoint.sh

# 暴露端口
EXPOSE 80

# 使用入口脚本
ENTRYPOINT ["/app/docker-entrypoint.sh"]