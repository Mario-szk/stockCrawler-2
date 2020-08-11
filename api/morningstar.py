import json
import time

import requests
from dateutil.parser import *

from api.config import MorningStar as msconfig


class MorningStar(object):
    def __init__(self) -> None:
        super().__init__()
        self.headers = {
            'Cookie': msconfig.cookie,
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
        }
        self.params = {'q': '002521',
                       'limit': '2',
                       'usid': 'false',
                       'type': 'fund'}

    def get_fund_fcid(self, fund_code):
        self.params['q'] = f'{fund_code}'
        response = requests.get('http://cn.morningstar.com/cacheapi/json/quickquery.ashx', headers=self.headers,
                                params=self.params, verify=False)
        data = response.text.replace("(", "").replace(")", "")
        data = json.loads(data)
        if len(data) > 0:
            data = data[0]
            return data['Key']
        return None

    def get_fund_detail(self, fid):
        params = {
            'command': 'portfolio',
            'fcid': f'{fid}'
        }
        response = requests.get('http://cn.morningstar.com/handler/quicktake.ashx', headers=self.headers, params=params,
                                verify=False)
        data = json.loads(response.text)
        data["EffectiveDate"] = data['EffectiveDate'].split("(")[1].split("+")[0]
        data["StyleBoxDate"] = data['StyleBoxDate'].split("(")[1].split("+")[0]
        return data


if __name__ == '__main__':
    # 1570691901
    # 15618240000
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1561824000.000))
    print(t)

    morningStar = MorningStar()
    fid = morningStar.get_fund_fcid("100038")
    print(fid)
    morningStar.get_fund_detail(fid)
