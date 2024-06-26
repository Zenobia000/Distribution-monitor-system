import datetime
import json
import typing

import pandas as pd
import requests


URL = "https://www.twse.com.tw/rwd/zh/fund/T86?date={}&selectType=ALL&response=json&_={}"

# 網頁瀏覽時, 所帶的 request header 參數, 模仿瀏覽器發送 request
HEADER = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Host": "www.twse.com.tw",
    "Referer": 'https://www.twse.com.tw/zh/page/trading/fund/T86.htmlsec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}


def crawler(parameters:typing.Dict[str, str]) -> pd.DataFrame:
    crawler_date = parameters.get("crawler_date", "")
    crawler_date = crawler_date.replace("-", "")
    crawler_timestamp = int(datetime.datetime.now().timestamp())

    resp = requests.get(
        url=URL.format(crawler_date, crawler_timestamp), headers=HEADER
    )

    columns = [
        "stock_id",
        "stock_name",
        "Foreign_Investors_include_Mainland_Area_Buy",
        "Foreign_Investors_include_Mainland_Area_Sell",
        "Foreign_Investors_include_Mainland_Area_Net",
        "Foreign_Dealer_Self_Buy",
        "Foreign_Dealer_Self_Sell",
        "Foreign_Dealer_Self_Net",
        "Investment_Trust_Buy",
        "Investment_Trust_Sell",
        "Investment_Trust_Net",
        "Dealer_Net",
        "Dealer_self_Buy",
        "Dealer_self_Sell",
        "Dealer_self_Net",
        "Dealer_Hedging_Buy",
        "Dealer_Hedging_Sell",
        "Dealer_Hedging_Net",
        "Total_Net",
    ]

    if resp.status_code == 200:

        resp = resp.content
        resp = resp.decode("utf-8-sig")

        resp_data = json.loads(resp)

        data = resp_data.get("data", "")

        data = pd.DataFrame(data, columns=columns)
        data["date"] = parameters.get("crawler_date", "")

    else:
        data = pd.DataFrame(columns=columns)

    return data


if __name__ == "__main__":
    parameters = {
        "crawler_date": "2024-01-26",
    }
    data = crawler(parameters)
    print(data)
