"""
按城市运行爬虫的命令行脚本

用法:
    python crawl_city.py fuzhou --limit 2000
    python crawl_city.py xiamen --limit 500
"""
import argparse
from crawler import crawl_city


def main():
    parser = argparse.ArgumentParser(
        description='安居客二手房爬虫 - 按城市爬取'
    )
    parser.add_argument(
        'city',
        help='安居客城市拼音，例如: fuzhou, xiamen, quanzhou'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='最大爬取条数，不指定则不限制'
    )

    args = parser.parse_args()
    crawl_city(args.city, limit=args.limit)


if __name__ == '__main__':
    main()
