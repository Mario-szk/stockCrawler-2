import json

import requests
from faker import Faker

url = "http://192.168.0.227:8081/api/people/create"


# 添加人员
def add_people(number):
    fake = Faker("zh_CN")
    data = {
        "faceSetId": "1",
        "peopleList": [

        ]
    }
    for i in range(number):
        data["peopleList"].append({
            "name": fake.name(),
            "code": fake.ean(length=8)
        }, )
    print(data)
    payload = json.dumps(data)
    headers = {
        'Content-Type': "application/json",
        'User-Agent': "PostmanRuntime/7.19.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "716714e9-b66a-4919-865b-044d9a16fb21,ebf4c84c-5d1e-40f1-8276-76fbb4a4c85c",
        'Host': "192.168.0.227:8081",
        'Accept-Encoding': "gzip, deflate",
        'Content-Length': "270",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

def run():
    pass


if __name__ == '__main__':
    add_people(100)
