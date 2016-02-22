#!/usr/bin/python
# -*- coding: utf-8 -*-
# 使用 Pushbullet 推送 Kindle 今日特价书

import requests
import re
import json

from bs4 import BeautifulSoup

url = 'http://www.amazon.cn'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}

def get_deals_page():
    html = requests.get(url, headers=headers)
    html = html.text.encode('utf-8')
    resurl = re.findall(r'"今日特价书","url":"(.+?)"', html)[0]
    resurl = url + resurl
    html = requests.get(resurl, headers=headers)
    content = html.text.encode('utf-8')
    return content

def get_useful_info(page):
    soup = BeautifulSoup(page, from_encoding="utf-8")

    for reviewStars in soup.find_all('div', attrs={'class': 'productReviewStars'}):
        reviewStars.decompose()

    for availability in soup.find_all('div', attrs={'class': 'productAvailability'}):
        availability.decompose()

    temp = soup.find_all('div', attrs={'class': 'gridProductContainer'})
    temp = str(temp)
    item = temp.replace('<div class="productByLine">', '作者:')
    s = BeautifulSoup(item, from_encoding="utf-8")
    text = s.get_text()
    res = " ".join(text.split()).encode('utf-8')
    return res[1:-1]

if __name__ == '__main__':
    page = get_deals_page()
    res = get_useful_info(page)

    PUSH_URL = 'https://api.pushbullet.com/v2/pushes'
    ACCESS_TOKEN = 'ACCESS_TOKEN'
    Headers = {'Access-Token': ACCESS_TOKEN, 'Content-Type': 'application/json'}

    postdata = {
        "type": "note",
        "title": "Kindle今日特价书",
        "body": res
    }

    r = requests.post(PUSH_URL, data = json.dumps(postdata), headers = Headers)
