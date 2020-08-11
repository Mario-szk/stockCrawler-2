import time

import numpy as np
import matplotlib.pyplot as plt

from api.mongodb import StockDB
from api.config import DbConfig


class TopStock(object):
    def get(self, rank, **kwargs):
        stockMongoDB = StockDB(DbConfig.dbName, DbConfig.dbStockTable)
        cursor = stockMongoDB.find_list(**kwargs)
        # data = {"0": {"name": "股票名字", "Symbol": "300347.SHE", "count": 0, "funds": [], "sectorName": []}}
        data = {}
        for i in cursor:
            if f"{rank}" != i["fund_rank"]:
                continue
            funds = {"fund_name": i["fund_name"], "fund_code": i["fund_code"], "fund_rank": i["fund_rank"]}
            if i["Symbol"] in data:
                mProperty = data[i["Symbol"]]
                mProperty["count"] += 1
                mProperty["funds"].append(funds)
                mProperty["sectorName"].append(i["SectorName"])
                mProperty["sectorName"] = list(set(mProperty["sectorName"]))
            else:
                mProperty = {"name": i["HoldingName"], "Symbol": i["Symbol"], "count": 1, "funds": [], "sectorName": []}
                mProperty["funds"].append(funds)
                mProperty["sectorName"].append(i["SectorName"])
                mProperty["sectorName"] = list(set(mProperty["sectorName"]))
                data[i["Symbol"]] = mProperty

        return data

    def deal(self, dataList, minCount, **args):
        name = []
        count = []
        symbol = []
        for i in dataList:
            data = dataList[i]
            print(data)
            if data["count"] < minCount:
                continue
            name.append(data["name"])
            count.append(data["count"])
            symbol.append(data["Symbol"])

        return {"title": args["title"], "name": dict(zip(name, count))}

    def run(self, star, number, **kwargs):
        print(kwargs)
        rank = self.get(star, **kwargs)

        if 'date' in kwargs:
            today = kwargs['date']
        else:
            today = time.strftime("%Y-%m-%d", time.localtime())
        return self.deal(rank, number, title=f"{today}持有{number}家{star}星级基金以上的股票", date=today)


def getData(star, min):
    topStock = TopStock()
    data = topStock.run(star, min)
    count = data["count"]
    symbol = data["symbol"]
    name = data["name"]
    index = np.arange(len(data["name"]))
    plt.figure(figsize=(20, 20))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title(data["title"], fontsize=40)
    plt.barh(index, count, facecolor='#ff9999', edgecolor='white')
    for x, y in zip(index, count):
        # ha: horizontal alignment
        # va: vertical alignment
        plt.text(y, x, y, fontsize=20)
        plt.text(0.02, x, symbol[x], fontsize=20)

    plt.yticks(index, name, fontsize=20)
    plt.xticks([])
    plt.savefig(f'./image/{data["title"]}.png')
    plt.show()
    # rank = getTopStock(star)
    # today = time.strftime("%Y-%m-%d", time.localtime())
    # showImg(rank, min, {"title": f"{today}持有{min}家{star}星级基金以上的股票"})


if __name__ == '__main__':
    getData(3, 3)
    getData(4, 3)
    getData(5, 3)
