import time

from flask import Flask, request

from web.utils.analysis import TopStock

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/TopStock')
def top_stock():
    topStock = TopStock()
    rank = request.args.get('rank', 5)
    number = request.args.get('number', 5)
    date = request.args.get('date', time.strftime("%Y-%m-%d", time.localtime()))

    return topStock.run(int(rank), int(number), date=date)


if __name__ == '__main__':
    app.run()
