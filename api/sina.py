import demjson
import requests


class SinaFund(object):
    def __init__(self) -> None:
        super().__init__()
        self.headers = {
            'Pragma': 'no-cache',
            'DNT': '1',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Accept': '*/*',
            'Referer': 'http://vip.stock.finance.sina.com.cn/fund_center/index.html',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
        }

        self.params = {
            'page': '2',
            'num': '40',
            'sort': 'starRating2y',
            'asc': '0',
            'ccode': '',
            'type': '1',
            'type3': '',
            'date': ''
        }
        self.url = 'http://vip.stock.finance.sina.com.cn/fund_center/data/jsonp.php/IO.XSRV2.CallbackList[\'rAFMA0MohkmJr2UO\']/FundRank_Service.getMSFundInfo'

    def get_fund_list(self, page) -> dict:
        self.params["page"] = page
        response = requests.get(self.url, headers=self.headers, params=self.params, verify=False)
        response.encoding="gb2312"
        data = response.text.split("((")[1].split("))")[0]
        jsonData = demjson.decode(data)
        data = jsonData["data"]
        if data is not None:
            return data
        else:
            return {}

    def get_top_stock(self):
        pass

    def __str__(self) -> str:
        return super().__str__()
