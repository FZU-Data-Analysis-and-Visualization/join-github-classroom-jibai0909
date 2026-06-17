"""
演示脚本：生成模拟房源数据，走通完整数据管道
（在实际教学中，将模拟数据替换为真实爬虫结果）

用法:
    python demo.py --count 2000
"""
import argparse
import random
from db import DB, TABLE_NAME


# 福州各市区的模拟数据池
DISTRICTS = {
    '晋安': 744,
    '仓山': 708,
    '台江': 376,
    '鼓楼': 70,
    '闽侯': 37,
    '连江': 30,
    '马尾': 12,
    '平潭': 11,
    '长乐': 9,
    '福清': 3,
}

LAYOUTS = ['1室1厅', '2室1厅', '2室2厅', '3室1厅', '3室2厅', '4室2厅', '5室2厅', '1室0厅']
AREAS = ['45㎡', '60㎡', '75㎡', '89㎡', '95㎡', '110㎡', '125㎡', '140㎡', '160㎡', '200㎡']
DIRECTIONS = ['南', '南北', '东南', '西南', '东', '西', '北', '东北', '西北']
FLOORS = ['低楼层/33层', '中楼层/18层', '高楼层/28层', '低楼层/6层', '中楼层/11层', '高楼层/33层']
AGES = ['2020年', '2018年', '2015年', '2010年', '2005年', '2000年', '1998年', '1995年']

# 各市区的小区名
COMMUNITIES = {
    '鼓楼': ['融侨锦江', '华林御景', '东街口小区', '西湖花园', '五四路小区'],
    '台江': ['万科金域中央', '中庚书香里', '茶亭国际', '金融街万达', '宝龙城市广场'],
    '仓山': ['融信大卫城', '金辉淮安半岛', '江南水都', '金山碧水', '海润滨江'],
    '晋安': ['万科城', '世茂云境', '保利香槟国际', '三盛国际公园', '东二环泰禾'],
    '马尾': ['名城银河湾', '阳光城翡丽湾', '名城港湾', '三木公园里'],
    '闽侯': ['阳光城西海岸', '中海寰宇天下', '万科又一城', '碧桂园贵安'],
    '连江': ['贵安新天地', '世纪金源', '凤翔国际'],
    '长乐': ['首占一号', '长乐万科城', '碧桂园'],
    '福清': ['融侨城', '龙旺名城', '中联城'],
    '平潭': ['世茂海峡城', '融信大卫城'],
}


def generate_demo_data(count=2000):
    """生成模拟的福州二手房数据并写入数据库"""
    db = DB()
    inserted = 0

    for district, weight in DISTRICTS.items():
        # 按比例分配各市区的房源数
        district_count = int(count * weight / sum(DISTRICTS.values()))
        if inserted + district_count > count:
            district_count = count - inserted

        communities = COMMUNITIES.get(district, ['某小区'])

        for _ in range(district_count):
            if inserted >= count:
                break

            area_val = random.choice(AREAS)
            area_num = float(area_val.replace('㎡', ''))
            unit_price = random.randint(8000, 45000)
            total_price = int(area_num * unit_price / 10000)

            data = {
                '城市': 'fuzhou',
                '市区': district,
                '标题': f'{random.choice(communities)} {random.choice(LAYOUTS)} 精装修',
                '户型': random.choice(LAYOUTS),
                '面积': area_val,
                '方位': random.choice(DIRECTIONS),
                '楼层': random.choice(FLOORS),
                '时间': f'{random.randint(1, 30)}天前发布',
                '所属小区': random.choice(communities),
                '所属区域': f'{district} - {random.choice(["东街口", "茶亭", "金山", "上街", "五四路", "火车站", "万达", "大学城", "东二环", "西湖"])}',
                '总价': f'{total_price}万',
                '均价': f'{unit_price}元/㎡',
                '房龄': random.choice(AGES),
            }
            db.insert_data(data)
            inserted += 1

            if inserted % 500 == 0:
                print(f'  已生成 {inserted} 条', flush=True)

    db.close()
    print(f'共生成 {inserted} 条模拟房源数据', flush=True)
    return inserted


def main():
    parser = argparse.ArgumentParser(description='生成模拟房源数据')
    parser.add_argument('--count', type=int, default=2000, help='生成数量（默认2000）')
    args = parser.parse_args()

    print(f'正在生成 {args.count} 条模拟数据...')
    generate_demo_data(args.count)

    print(f'\n数据已写入 SQLite 数据库')
    print(f'下一步: python export_csv.py 导出 CSV')


if __name__ == '__main__':
    main()
