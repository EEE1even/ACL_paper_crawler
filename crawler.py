# -*- coding: utf-8 -*-
# @Time    : 2024/12/16 16:29
# @Author  : Eleven
# @File    : crawler.py
import requests
from bs4 import BeautifulSoup
import argparse

def crawler():
    parser = argparse.ArgumentParser(description='Crawl ACL papers')
    parser.add_argument('--year',required=True,help='Year of the ACL event')
    parser.add_argument('--keyword',required=True,help='keywords about what paper you want to crawl')
    args = parser.parse_args()

    year = args.year
    keyword = args.keyword

    url = f"https://aclanthology.org/events/acl-{year}/"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # 可以在这里指定多个分区的ID
    target_div_ids = [f"{year}acl-long", f"{year}acl-short"]
    base_url = "https://aclanthology.org"

    for div_id in target_div_ids:
        target_div = soup.find('div', id=div_id)
        if target_div:
            print(f"正在从分区 {div_id} 中爬取数据...")
            links = target_div.select('a.align-middle')
            for a_tag in links:
                title = a_tag.get_text(strip=True)
                href = a_tag.get('href')
                if href and title:
                    full_url = base_url + href
                    # 关键字过滤逻辑
                    if keyword.lower() in title.lower():
                        print(title, full_url)
            print(f"完成分区 {div_id} 的爬取。\n")
        else:
            print(f"分区 {div_id} 未找到！\n")

if __name__ == '__main__':
    crawler()