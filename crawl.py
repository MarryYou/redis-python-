# coding:utf-8
from bs4 import BeautifulSoup
import requests
import json
from data_base import RedisClient

def crawl():
    url = 'http://www.xicidaili.com/nn/'
    headers = {
        'Host': 'www.xicidaili.com',
        'Referer': 'http://www.xicidaili.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    ip_list = []
    redis_client = RedisClient()
    for index in range(1, 5):
        res = requests.get(url=url+str(index), headers=headers, timeout=3)
        html = BeautifulSoup(res.text, 'lxml').find_all(
            'table', attrs={'id': 'ip_list'})
        table_info = BeautifulSoup(str(html), 'lxml').find_all('tr')
        for sub in range(1, len(table_info)):
            ip_Content = str(
                table_info[sub].contents[3].text) + ":" + str(table_info[sub].contents[5].text)
            ip_list.append(ip_Content)
    for proxy in ip_list:
        redis_client.add(proxy)   
    
