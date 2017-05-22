import requests
from bs4 import BeautifulSoup


TWSE_URL = 'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAYMAIN.php'


def get_web_content(query_data):
    resp = requests.post(TWSE_URL, data=query_data)
    if resp.status_code != 200:
        return None
    else:
        return BeautifulSoup(resp.text, 'html.parser')


def get_data(stock_id, year, month):
    year = str(year)
    month = '0' + str(month) if month < 10 else str(month)
    query_data = {
        'query_year': year,
        'query_month': month,
        'CO_ID': stock_id
    }
    info = list()
    dom = get_web_content(query_data)
    if dom is None:
        return None
    else:
        for tr in dom.find('table').tbody.find_all('tr'):
            # 日期, 成交股數, 成交金額, 開盤價, 最高價, 最低價, 收盤價, 漲跌價差, 成交筆數
            tds = tr.find_all('td')
            info.append((tds[0].text, tds[3].text, tds[6].text, tds[7].text, tds[8].text))
        return info


def main():
    year = 2017
    stock_id = '2330'
    collected_info = list()
    for month in range(1, 5):
        print('Processing', year, month)
        collected_info.append(get_data(stock_id, year, month))
    print('Date, Opening Price, Closing Price, Trading Range, Turnover')
    for info in collected_info:
        for data in info:
            print(data)


if __name__ == '__main__':
    main()
