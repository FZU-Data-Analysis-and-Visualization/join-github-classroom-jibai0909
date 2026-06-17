"""
从 MySQL 数据库导出房源数据到 CSV 文件

用法:
    python export_csv.py

输出:
    ershoufang_list.csv（utf-8-sig 编码，Excel 可直接打开）
"""
import csv
from db import DB, TABLE_NAME

OUTPUT_FILE = 'ershoufang_list.csv'


def export():
    db = DB()
    cursor = db.cursor

    # 查询所有数据
    cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    # 写入 CSV（utf-8-sig 编码，确保 Excel 正确显示中文）
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(rows)

    db.close()
    print(f'Exported {len(rows)} rows to {OUTPUT_FILE}')


if __name__ == '__main__':
    export()
