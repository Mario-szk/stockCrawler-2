import time

import pymongo


class MongoDB(object):
    def __init__(self, db_name, collection_name) -> None:
        super().__init__()
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def update_one_sync(self, data):
        uptime = time.strftime("%Y-%m-%d", time.localtime())
        for line in data:
            line["update_at"] = uptime
            print(line)
            self.collection.update_one(line, {'$set': line}, upsert=True)


class FundDB(MongoDB):
    def __init__(self, db_name, collection_name) -> None:
        super().__init__(db_name, collection_name)

    def find_fund_list(self, star):
        today = time.strftime("%Y-%m-%d", time.localtime())
        query = {"starRating5y": {"$gte": f"{star}"}, "update_at": today}
        res = self.collection.find(query)
        return res


class StockDB(MongoDB):
    def __init__(self, db_name, collection_name) -> None:
        super().__init__(db_name, collection_name)

    def find_list(self, **kwargs):
        if 'date' in kwargs:
            today = kwargs['date']
        else:
            today = time.strftime("%Y-%m-%d", time.localtime())
        query = {"update_at": today}
        res = self.collection.find(query)
        return res
