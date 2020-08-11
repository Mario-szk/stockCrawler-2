**安装 mongodb**

https://docs.mongodb.com/manual/installation/

**编辑 api/config 文件**

```python
class MorningStar(object):
    cookie = "authWeb="
```
去晨星网站注册账号，并查看cookie，找到 authWeb 字段填入

如：
```python
class MorningStar(object):
    cookie = "authWeb=674676000C571713DFF15FCC656FB738913....."
```

**python3 stock.py**

进行爬取数据

**运行web**
`export FLASK_APP=web/index.py`

`flask run --host=0.0.0.0`