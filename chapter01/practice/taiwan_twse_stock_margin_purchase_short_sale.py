import datetime
import json
import typing

import pandas as pd
import requests

URL = "https://www.twse.com.tw/exchangeReport/MI_MARGN?response=json&date={}&selectType=ALL&_={}"

# 網頁瀏覽時, 所帶的 request header 參數, 模仿瀏覽器發送 request
HEADER = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Host": "www.twse.com.tw",
    "Referer": "https://www.twse.com.tw/zh/page/trading/exchange/MI_MARGN.html",
    "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}


def crawler(parameters: typing.Dict[str, str]) -> pd.DataFrame:
    crawler_date = parameters.get("crawler_date", "")
    crawler_date = crawler_date.replace("-", "")
    crawler_timestamp = int(datetime.datetime.now().timestamp())

    resp = requests.get(
        url=URL.format(crawler_date, crawler_timestamp), headers=HEADER
    )

    '''
    stock_id - 證券代號：股票的唯一識別代碼。
    stock_name - 證券名稱：股票的名稱。
    Foreign_Investors_include_Mainland_Area_Buy - 外陸資買進股數(不含外資自營商)：指來自外地（包括大陸地區）的投資者購買的股份數量，不包括外資自營商的購買。
    Foreign_Investors_include_Mainland_Area_Sell - 外陸資賣出股數(不含外資自營商)：指來自外地（包括大陸地區）的投資者售出的股份數量，不包括外資自營商的售出。
    Foreign_Investors_include_Mainland_Area_Net - 外陸資買賣超股數(不含外資自營商)：來自外地（包括大陸地區）的投資者的淨買賣股份數量，即購買減去售出的數量，不包括外資自營商的交易。
    Foreign_Dealer_Self_Buy - 外資自營商買進股數：外資自營商購買的股份數量。
    Foreign_Dealer_Self_Sell - 外資自營商賣出股數：外資自營商售出的股份數量。
    Foreign_Dealer_Self_Net - 外資自營商買賣超股數：外資自營商的淨買賣股份數量，即購買減去售出的數量。
    Investment_Trust_Buy - 投信買進股數：投資信託購買的股份數量。
    Investment_Trust_Sell - 投信賣出股數：投資信託售出的股份數量。
    Investment_Trust_Net - 投信買賣超股數：投資信託的淨買賣股份數量，即購買減去售出的數量。
    Dealer_Net - 自營商買賣超股數：自營商的淨買賣股份數量，綜合所有自營商活動的總淨結果。
    Dealer_self_Buy - 自營商買進股數(自行買賣)：自營商為自己的賬戶買入的股份數量。
    Dealer_self_Sell - 自營商賣出股數(自行買賣)：自營商為自己的賬戶賣出的股份數量。
    Dealer_self_Net - 自營商買賣超股數(自行買賣)：自營商為自己的賬戶的淨買賣股份數量，即購買減去售出的數量。
    Dealer_Hedging_Buy - 自營商買進股數(避險)：自營商出於避險目的購買的股份數量。
    Dealer_Hedging_Sell - 自營商賣出股數(避險)：自營商出於避險目的賣出的股份數量。
    Dealer_Hedging_Net - 自營商買賣超股數(避險)：自營商出於避險目的的淨買賣股份數量，即購買減去售出的數量。
    Total_Net - 三大法人買賣超股數：三大法人（外資、投信、自營商）的淨買賣股份數量的總和。
    date - 日期：數據的日期。

    '''

    columns = [
        "stock_id",
        "stock_name",
        "MarginPurchaseBuy",
        "MarginPurchaseSell",
        "MarginPurchaseCashRepayment",
        "MarginPurchaseYesterdayBalance",
        "MarginPurchaseTodayBalance",
        "MarginPurchaseLimit",
        "ShortSaleBuy",
        "ShortSaleSell",
        "ShortSaleCashRepayment",
        "ShortSaleYesterdayBalance",
        "ShortSaleTodayBalance",
        "ShortSaleLimit",
        "OffsetLoanAndShort",
        "Note",
    ]
    if resp.ok:
        resp_data = json.loads(resp.text)
        data = resp_data.get("data", "")
        data = pd.DataFrame(data, columns=columns)
        data["date"] = parameters.get("crawler_date", "")
    else:
        data = pd.DataFrame(columns=columns)
    return data


if __name__ == "__main__":
    parameters = {
        "crawler_date": "2022-01-26",
    }
    data = crawler(parameters)
    print(data)
