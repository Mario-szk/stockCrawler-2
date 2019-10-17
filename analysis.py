import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from api.mongodb import MongoDB, StockDB
from config import DbConfig


def getTopStock(rank):
    stockMongoDB = StockDB(DbConfig.dbName, DbConfig.dbStockTable)
    cursor = stockMongoDB.find_list()
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


def saveToCsv(data):
    pass


def showImg(dataList, minCount, args):
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
    print(name)
    print(len(name))
    index = np.arange(len(name))
    plt.figure(figsize=(20, 20))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title(args["title"], fontsize=40)
    plt.barh(index, count, facecolor='#ff9999', edgecolor='white')
    for x, y in zip(index, count):
        # ha: horizontal alignment
        # va: vertical alignment
        plt.text(y, x, y, fontsize=20)
        plt.text(0.02, x , symbol[x], fontsize=20)

    plt.yticks(index, name, fontsize=20)
    plt.xticks([])
    plt.savefig(f'./{args["title"]}.png')
    plt.show()


def getData(star, min):
    rank = getTopStock(star)
    showImg(rank, min, {"title": f"持有{min}家{star}星级基金以上的股票"})


if __name__ == '__main__':
    getData(3, 3)
    getData(4, 3)
    getData(5, 3)
