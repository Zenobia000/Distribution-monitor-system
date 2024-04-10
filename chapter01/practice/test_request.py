import requests

headers = {
    "Host": "www.twse.com.tw",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}


# 使用前面定義的 headers dictionary
response = requests.get('http://www.twse.com.tw/rwd/zh/fund/T86?date=20240401&selectType=ALL&response=json', headers=headers)

# 打印回應的文字內容
print(response.text)

