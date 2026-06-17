"""
项目配置文件
使用 SQLite 数据库（无需安装 MySQL），Chrome 浏览器也不需要
"""

import os

# SQLite 数据库文件路径（项目根目录下）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'ershoufang.db')

# 需要爬取的城市列表（main.py 使用）
# 城市名使用安居客URL中的拼音子域名
CITY_LIST = [
    'fuzhou',
    'xiamen',
    'quanzhou',
]
