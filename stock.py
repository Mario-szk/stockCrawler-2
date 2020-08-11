from api.mongodb import FundDB, MongoDB
from api.morningstar import MorningStar
from api.sina import SinaFund
from api.config import DbConfig


def get_fund():
    data_list = []
    sinaFund = SinaFund()
    for i in range(1, 1000):
        data = sinaFund.get_fund_list(i)
        if len(data) < 1:
            print(f"第{i}页无数据，结束。")
            break
        else:
            print(f"第{i}页有数据，长度：{len(data)}。")
            data_list.extend(data)
    print(len(data_list))
    print(data_list)
    return data_list


def save_fund(data):
    fundDB = FundDB(DbConfig.dbName, DbConfig.dbFundTable)
    fundDB.update_one_sync(data)


def update_fund_list():
    data = get_fund()
    save_fund(data)


def update_stock_list():
    """
    更新股票数据
    :return:
    """

    fundDB = FundDB(DbConfig.dbName, DbConfig.dbFundTable)
    data = fundDB.find_fund_list(1)
    morningStar = MorningStar()
    stockMongoDB = MongoDB(DbConfig.dbName, DbConfig.dbStockTable)
    bondMongoDB = MongoDB(DbConfig.dbName, DbConfig.dbBondTable)
    bond_hold_data_list = []
    stock_hold_data_list = []
    for line in data:
        print(line)
        fcid = morningStar.get_fund_fcid(line['symbol'])
        data = morningStar.get_fund_detail(fcid)
        fund_name = line['name']
        fund_code = line['symbol']
        fund_rank = line['starRating5y']
        fund_public_data = data['EffectiveDate']
        top10StockHoldings = data["Top10StockHoldings"]
        top5BondHoldings = data["Top5BondHoldings"]
        print(data)
        for stock in top10StockHoldings:
            stock["fund_name"] = fund_name
            stock["fund_code"] = fund_code
            stock["fund_rank"] = fund_rank
            stock["fund_public_data"] = fund_public_data
            stock_hold_data_list.append(stock)
        for bond in top5BondHoldings:
            bond["fund_name"] = fund_name
            bond["fund_code"] = fund_code
            bond["fund_rank"] = fund_rank
            bond["fund_public_data"] = fund_public_data
            bond_hold_data_list.append(bond)

    stockMongoDB.update_one_sync(stock_hold_data_list)
    bondMongoDB.update_one_sync(bond_hold_data_list)


if __name__ == '__main__':
    update_fund_list()
    update_stock_list()

# NB. Original query string below. It seems impossible to parse and
# reproduce query strings 100% accurately so the one below is given
# in case the reproduced version is not "correct".
# response = requests.get('http://vip.stock.finance.sina.com.cn/fund_center/data/jsonp.php/IO.XSRV2.CallbackList^\['rAFMA0MohkmJr2UO'^\]/FundRank_Service.getMSFundInfo?page=2^&num=40^&sort=starRating2y^&asc=0^&ccode=^&type=1^&type3=^&date=', headers=headers, cookies=cookies, verify=False)
