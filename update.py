import requests
import json
from config import rd


def update_province_data():
    url = 'http://api.tianapi.com/txapi/ncovcity/index?key=41d70b21767cd950e6638d1be3fcbf11'
    res = requests.get(url).json()
    rd.set('ncovcity_data', json.dumps(res))
    return res


def update_news_data():
    url = 'http://api.tianapi.com/txapi/ncov/index?key=41d70b21767cd950e6638d1be3fcbf11'
    res = requests.get(url).json()
    rd.set('ncov_all_data', json.dumps(res))
    return res


def update_global_data():
    url = 'https://interface.sina.cn/news/wap/fymap2020_data.d.json'
    res = requests.get(url).json()
    rd.set('ncov_global_data', json.dumps(res))
    return res


def update_nocv_data():
    headers = {
        'user-agent': '',
        'accept': ''
    }
    url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total'
    res = requests.get(url, headers=headers).json()
    rd.set('ncov_data', json.dumps(res))
    return res


update_province_data()
#update_news_data()
update_nocv_data()
update_global_data()
