#!/bin/bash

# 等待MySQL启动
until mysqladmin ping -h"$MYSQL_HOST" -P"$MYSQL_PORT" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --silent; do
    >&2 echo "MySQL is unavailable - sleeping"
    sleep 1
done

>&2 echo "MySQL is up - executing command"

# 执行数据库迁移
python manage.py migrate

# 收集静态文件
python manage.py collectstatic --noinput

# 启动Gunicorn
exec gunicorn config.wsgi:application \
    --name inspection_app \
    --bind 0.0.0.0:80 \
    --workers 2 \
    --threads 4 \
    --worker-class gthread \
    --worker-tmp-dir /dev/shm \
    --log-level=info \
    --access-logfile=/app/logs/gunicorn-access.log \
    --error-logfile=/app/logs/gunicorn-error.log \
    --timeout 60 \
    --max-requests 1000 \
    --max-requests-jitter 50