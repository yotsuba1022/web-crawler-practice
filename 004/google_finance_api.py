import requests
import json
from datetime import datetime, timedelta


GOOGLE_FINANCE_API_URL = 'http://finance.google.com/finance/info?client=ig&q='
GOOGLE_FINANCE_HISTORY_API_URL = 'http://www.google.com/finance/getprices?q='


def get_stock(query):
    # You can query for multiple stocks by splitting with ","
    resp = requests.get(GOOGLE_FINANCE_API_URL + query)
    if resp.status_code != 200:
        print('Invalid url or query param: ' + resp.url)
        return None
    else:
        # Need to remove the redundant chars '//' at the head of response
        return json.loads(resp.text.replace('//', ''))


def get_stock_history(stock_id, stock_mkt):
    resp = requests.get(GOOGLE_FINANCE_HISTORY_API_URL + stock_id + '&x=' + stock_mkt + '&i=86400&p=1M')
    ''' e.g.,
    EXCHANGE%3DTPE
    MARKET_OPEN_MINUTE=540
    MARKET_CLOSE_MINUTE=810
    INTERVAL=86400
    COLUMNS=DATE,CLOSE,HIGH,LOW,OPEN,VOLUME
    DATA=
    TIMEZONE_OFFSET=480
    a1488346200,186,188.5,186,188.5,46176000
    1,186,188.5,185,188,39914000
    2,184,185,184,184.5,28085000
    5,183.5,184.5,183.5,184,12527000
    ...
    '''
    index = -1
    records = resp.text.split('\n')
    for record in records:
        # 'a' means the start point of stock information
        if record.startswith('a'):
            index = records.index(record)
            break
    if index > 0:
        records = records[index:]
        # To transform the unix time to human readable time at the first line of stock info
        unix_time = int(records[0].split(',')[0][1:])
        init_time = datetime.fromtimestamp(unix_time)

        # To handle to first row
        first_row = records[0].split(',')
        first_row[0] = init_time

        history = list()
        history.append(first_row)

        # To handle the rest of stock records
        for record in records[1:]:
            if record:
                data = record.split(',')
                delta = int(data[0])
                data[0] = init_time + timedelta(days=delta)
                history.append(data)
        return history
    else:
        return None


def main():
    query = 'TPE:2330'
    print('Real time stock price for ' + query)
    stocks = get_stock(query)
    print(stocks[0])
    print('\n')
    stock_id = '2330'
    stock_mkt = 'TPE'
    print('Stock price history for ' + stock_mkt + ":" + stock_id)
    print('(Date, Close, High, Low, Open, Volume)')
    history = get_stock_history(stock_id, stock_mkt)
    for hist in history:
        print(hist[0].strftime("%Y/%m/%d"), hist[1:])


if __name__ == '__main__':
    main()

