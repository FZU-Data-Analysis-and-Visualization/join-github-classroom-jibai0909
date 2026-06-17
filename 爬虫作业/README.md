# 安居客二手房爬虫 (anjuke-crawler)

基于 Selenium + BeautifulSoup 的安居客二手房数据爬虫，支持将爬取结果写入 MySQL 并导出 CSV。

## 项目结构

```
anjuke-crawler/
├── README.md           # 项目说明
├── requirements.txt    # Python 依赖包列表
├── config.py           # 数据库连接配置、城市列表
├── db.py               # MySQL 建表、插入数据
├── crawler.py          # 爬虫核心逻辑
├── crawl_city.py       # 按城市运行爬虫（课堂推荐）
├── export_csv.py       # 从 MySQL 导出 CSV
└── main.py             # 批量爬取多个城市
```

## 环境要求

- Python 3.11+
- Google Chrome 浏览器
- MySQL 数据库

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 创建数据库

```sql
CREATE DATABASE IF NOT EXISTS ershoufang CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 修改配置

编辑 `config.py`，将 `password` 改为你的 MySQL 密码。

### 4. 运行爬虫

爬取福州 2000 条数据：

```bash
python crawl_city.py fuzhou --limit 2000
```

### 5. 导出 CSV

```bash
python export_csv.py
```

### 6. 统计市区房源数

```bash
python -c "import csv, collections; rows=list(csv.DictReader(open('ershoufang_list.csv', encoding='utf-8-sig'))); c=collections.Counter((r.get('市区') or '未识别').strip() or '未识别' for r in rows); print('TOTAL', len(rows)); [print(k, v) for k,v in c.most_common()]"
```

## 数据字段

| 字段 | 说明 |
|------|------|
| 城市 | 城市拼音 |
| 市区 | 提取的区县名 |
| 标题 | 房源标题 |
| 户型 | 户型信息 |
| 面积 | 房屋面积 |
| 方位 | 朝向 |
| 楼层 | 楼层信息 |
| 时间 | 发布时间 |
| 所属小区 | 小区名称 |
| 所属区域 | 详细区域地址 |
| 总价 | 房屋总价 |
| 均价 | 每平米均价 |
| 房龄 | 建成年份 |

## 课堂使用注意

- 课堂演示建议限制数据量（如 100、500、2000 条）
- 请求间隔已设 `time.sleep(3)`，避免高频请求
- 仅用于课程学习和数据分析示范
- 遵守网站服务条款

## 参考链接

- 项目仓库: https://github.com/weijiayi-1/anjuke-crawler
- Selenium 文档: https://www.selenium.dev/documentation/
