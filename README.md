# 巡检系统后端

这是一个基于 Django 开发的巡检系统后端服务。

## 功能特点

- 用户认证与授权
- 巡检记录管理
- 事件记录与追踪
- 数据统计与分析
- RESTful API 接口

## 技术栈

- Python 3.8+
- Django 4.0+
- Django REST framework
- SQLite（开发环境）

## 开发环境设置

1. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行数据库迁移：
```bash
python manage.py migrate
```

4. 启动开发服务器：
```bash
python manage.py runserver
```

## API 文档

启动服务器后，访问 http://localhost:8000/api/docs/ 查看详细的 API 文档。

## 许可证

MIT License 