"""
数据库操作模块（使用 SQLite，免安装）
负责建表、插入数据、查询数据
"""
import sqlite3
from config import DB_PATH

TABLE_NAME = 'ershoufang_list'

# 数据字段列表（对应最终 CSV 的列）
FIELDS = [
    '城市', '市区', '标题', '户型', '面积', '方位', '楼层', '时间',
    '所属小区', '所属区域', '总价', '均价', '房龄'
]

# 建表 SQL（SQLite 语法）
CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    城市 TEXT,
    市区 TEXT,
    标题 TEXT,
    户型 TEXT,
    面积 TEXT,
    方位 TEXT,
    楼层 TEXT,
    时间 TEXT,
    所属小区 TEXT,
    所属区域 TEXT,
    总价 TEXT,
    均价 TEXT,
    房龄 TEXT
)
"""


class DB:
    """SQLite 数据库操作封装（文件型数据库，无需安装服务端）"""

    def __init__(self, db_path=None):
        path = db_path or DB_PATH
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        # 自动建表
        self.cursor.execute(CREATE_TABLE_SQL)
        self.conn.commit()

    def insert_data(self, data: dict):
        """
        将一条房源数据（Python 字典）插入数据库

        参数:
            data: 包含字段名和值的字典
        示例:
            data = {
                '城市': 'fuzhou',
                '市区': '鼓楼',
                '标题': '某小区二手房',
                '总价': '300万'
            }
        """
        placeholders = ','.join(['?'] * len(FIELDS))
        keys = ','.join(FIELDS)
        sql = f"INSERT INTO {TABLE_NAME} ({keys}) VALUES ({placeholders})"
        vals = [data.get(f, '') for f in FIELDS]
        self.cursor.execute(sql, vals)
        self.conn.commit()

    def count(self):
        """返回当前表的总行数"""
        self.cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
        return self.cursor.fetchone()[0]

    def fetch_all(self):
        """返回表中所有数据"""
        self.cursor.execute(f"SELECT * FROM {TABLE_NAME}")
        return self.cursor.fetchall()

    def fetch_columns(self):
        """返回表的列名"""
        self.cursor.execute(f"SELECT * FROM {TABLE_NAME} LIMIT 0")
        return [desc[0] for desc in self.cursor.description]

    def close(self):
        """关闭数据库连接"""
        self.cursor.close()
        self.conn.close()
