# FireHydrant 消防栓后端工程文件

## 简介
一款任务中心平台的后台服务

## 技术选型
环境: Kubernetes v1.10.11  
包管理: Helm
持续集成: Jenkins
系统: ubuntu 16.04
后端框架: Django 2.1.2
消息队列: RabbitMQ
任务队列: Celery
缓存集群: Redis-cluster
数据库:  Mariadb

## 目录简介
├── FireHydrant         系统文件夹
│   ├── __init__.py
│   ├── __pycache__
│   ├── settings.py     设置文件
│   ├── urls.py         路由文件
│   └── wsgi.py
├── common              工具文件夹
│   ├── __init__.py
│   ├── __pycache__
│   ├── constants       常量
│   ├── core            功能工具
│   ├── decorate        装饰器
│   ├── dispatchers     异步调度文件
│   ├── entity          建模信息对象
│   ├── enum            枚举数据集
│   ├── exceptions      异常文件夹
│   ├── middlewares     系统中间件
│   └── utils           工具
├── config.yml          配置文件
├── data                数据
│   └── static          静态文件
├── db.sqlite3
├── gunicorn_server.py  gunicorn启动文件
├── manage.py
├── server              业务文件夹
│   ├── __init__.py
│   ├── __pycache__
│   ├── account         账户模块
│   ├── pay             支付模块
│   ├── ranking         排行模块
│   ├── task            任务模块
│   └── team            组队模块
└── templates

## PS
当前文件不包含部署文件内容