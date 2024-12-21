#!/bin/bash

# 等待PostgreSQL启动
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "PostgreSQL is up - executing command"

# 执行数据库迁移
python manage.py migrate

# 收集静态文件
python manage.py collectstatic --noinput

# 启动Gunicorn
exec gunicorn config.wsgi:application \
    --name inspection_app \
    --bind 0.0.0.0:80 \
    --workers 3 \
    --threads 2 \
    --worker-class gthread \
    --worker-tmp-dir /dev/shm \
    --log-level=info \
    --access-logfile=- \
    --error-logfile=- 