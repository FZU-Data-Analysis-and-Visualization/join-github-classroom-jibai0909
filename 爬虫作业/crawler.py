"""
爬虫核心逻辑模块（使用 Selenium + Chrome + selenium-stealth 绕过反爬）
负责打开网页、解析 HTML、提取房源数据字段

依赖：Google Chrome 浏览器 + 项目目录下的 chromedriver.exe
"""
import os
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from bs4 import BeautifulSoup
from db import DB


def extract_district(address_text):
    """
    从「所属区域」文本中提取第一个区县名称

    示例:
        '鼓楼 - 东街口'  →  '鼓楼'
        '台江-茶亭'      →  '台江'
        '闽侯县 上街'    →  '闽侯县'
        '仓山/金山'      →  '仓山'
    """
    text = re.sub(r'\s+', ' ', address_text).strip()
    if not text:
        return ''

    parts = [part.strip() for part in re.split(r'[-－–—·/|\s]+', text) if part.strip()]
    district = parts[0] if parts else text.split()[0]

    return district


def crawl_city(city_pinyin, limit=None):
    """
    爬取指定城市的二手房数据

    参数:
        city_pinyin: 城市拼音，例如 'fuzhou'、'xiamen'
        limit: 最大爬取条数，None 表示不限制

    返回:
        inserted_count: 实际插入的条数
    """
    print(f'正在爬取: {city_pinyin}')

    # 初始化数据库连接
    db = DB()

    # 配置 Chrome
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])

    # 使用本地下载的 ChromeDriver
    driver_path = os.path.join(os.path.dirname(__file__), 'chromedriver.exe')
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # 应用 stealth 反检测
    stealth(
        driver,
        languages=['zh-CN', 'zh'],
        vendor='Google Inc.',
        platform='Win32',
        webgl_vendor='Intel Inc.',
        renderer='Intel Iris OpenGL Engine',
        fix_hairline=True,
    )

    inserted_count = 0

    try:
        # 遍历房龄筛选条件 (y1 ~ y5)
        for y in range(1, 6):
            if limit is not None and inserted_count >= limit:
                break

            # 遍历页码
            for p in range(1, 51):  # 最多 50 页
                if limit is not None and inserted_count >= limit:
                    print(f'已达到限制: {inserted_count}', flush=True)
                    return inserted_count

                url = f'https://{city_pinyin}.anjuke.com/sale/p{p}-y{y}/?from=fangjia'
                print(f'{url} (y={y}, p={p})', flush=True)

                driver.get(url)
                time.sleep(3)

                # 检查是否被重定向到验证码页面
                if 'captcha' in driver.current_url or 'antispam' in driver.current_url:
                    print(f'  触发反爬验证，等待后重试...', flush=True)
                    time.sleep(5)
                    continue

                soup = BeautifulSoup(driver.page_source, 'lxml')

                # 找到房源列表
                soup_list = soup.select('.property')
                if not soup_list:
                    print(f'第 {p} 页没有找到房源，可能已到最后一页')
                    break

                for sl in soup_list:
                    if limit is not None and inserted_count >= limit:
                        break

                    try:
                        data = {}

                        # 城市
                        data['城市'] = city_pinyin

                        # 标题
                        title_els = sl.select('.property-content-title-name')
                        data['标题'] = title_els[0].text.strip() if title_els else 'N/A'

                        # 获取所有信息文本（新版安居客结构）
                        # .property-content-info-text 包含: [0]户型(带attribute), [1]面积, [2]方位, [3]楼层, [4]建造时间
                        info_texts = [el.text.strip() for el in sl.select('.property-content-info-text')]

                        # 户型（带 property-content-info-attribute 类的那个）
                        layout_el = sl.select_one('.property-content-info-attribute')
                        data['户型'] = layout_el.text.strip() if layout_el else 'N/A'

                        # 跳过第一个（户型），取后面的: 面积, 方位, 楼层, 房龄
                        detail_items = info_texts[1:] if len(info_texts) > 1 else []
                        data['面积'] = detail_items[0] if len(detail_items) > 0 else 'N/A'
                        data['方位'] = detail_items[1] if len(detail_items) > 1 else 'N/A'
                        data['楼层'] = detail_items[2] if len(detail_items) > 2 else 'N/A'
                        data['时间'] = detail_items[3] if len(detail_items) > 3 else 'N/A'
                        data['房龄'] = detail_items[4] if len(detail_items) > 4 else detail_items[3] if len(detail_items) > 3 else 'N/A'

                        # 所属小区
                        comm_el = sl.select_one('.property-content-info-comm-name')
                        data['所属小区'] = comm_el.get_text(strip=True) if comm_el else 'N/A'

                        # 所属区域
                        addr_el = sl.select_one('.property-content-info-comm-address')
                        data['所属区域'] = addr_el.get_text(' ', strip=True) if addr_el else 'N/A'

                        # 总价
                        total_price_el = sl.select_one('.property-price-total')
                        data['总价'] = total_price_el.get_text(strip=True) if total_price_el else 'N/A'

                        # 均价
                        unit_price_el = sl.select_one('.property-price-average')
                        data['均价'] = unit_price_el.text.strip() if unit_price_el else 'N/A'

                        # 从所属区域中提取市区
                        data['市区'] = extract_district(data['所属区域'])

                        # 写入数据库
                        db.insert_data(data)
                        inserted_count += 1

                        if inserted_count % 100 == 0:
                            print(f'  已插入 {inserted_count} 条', flush=True)

                    except Exception as e:
                        print(f'  解析单条房源出错: {e}', flush=True)
                        continue

                print(p, flush=True)

    finally:
        driver.quit()
        db.close()

    print(f'本次新增: {inserted_count}', flush=True)
    return inserted_count
