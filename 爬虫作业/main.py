"""
批量爬取多个城市的入口脚本
按 config.py 中 CITY_LIST 配置的城市列表依次爬取

注意:
    课堂演示建议使用 crawl_city.py 按单个城市和指定条数运行:
        python crawl_city.py fuzhou --limit 2000
"""
from config import CITY_LIST
from crawler import crawl_city


def main():
    print(f'计划爬取城市: {CITY_LIST}')
    for city in CITY_LIST:
        print(f'\n{"=" * 50}')
        crawl_city(city)
        print(f'{"=" * 50}\n')


if __name__ == '__main__':
    main()
