import requests
from bs4 import BeautifulSoup

# To query the specific stock info, add "MARKET:STOCK_ID" after the url.
# e.g.: https://www.google.com/finance?q=[MARKET]:[STOCK_ID]
GOOGLE_FINANCE_INFO = "https://www.google.com/finance?q="
GOOGLE_FINANCE_HISTORY = "https://www.google.com/finance/historical?q="
CODE_TSMC = "TPE:2330"
FINANCE_HISTORY_START_BASE = 30
FINANCE_HISTORY_RECORD_SIZE = 30


def get_web_page(url, query):
    if query:
        resp = requests.get(url+query)
    else:
        resp = requests.get(url)

    if resp.status_code != 200:
        print('Invalid url: ', resp.url)
        return None
    else:
        return resp.text


def get_stock_info(dom):
    soup = BeautifulSoup(dom, 'html5lib')
    stock = dict()
    stock['name'] = soup.title.text.split(':')[0]
    stock['current_price'] = soup.find(id='price-panel').span.span.text
    stock['current_change'] = soup.find(id='price-panel').find('div', 'id-price-change').text.strip().replace('\n', '')
    for table in soup.find('div', 'snap-panel').find_all('table'):
        for tr in table.find_all('tr'):
            key = tr.find('td', 'key').text.lower().strip()
            value = tr.find('td', 'val').text.strip()
            stock[key] = value
    return stock


def get_stock_history(dom):
    soup = BeautifulSoup(dom, 'html5lib')
    table = soup.find('table', 'historical_price')
    header_row = table.find('tr', 'bb')
    headers = [header for header in header_row.stripped_strings]
    print(headers)
    for tds in table.find_all('tr')[1:]:
        print([data for data in tds.stripped_strings])


def main():
    finance_info_page = get_web_page(GOOGLE_FINANCE_INFO, CODE_TSMC)
    if finance_info_page:
        stock = get_stock_info(finance_info_page)
        for k, v in stock.items():
            print(k + ":", v)

    # To fetch history data by pagination, you need to add two query params: start and num.
    # Just like the following link:
    # https://www.google.com/finance/historical?q=TPE:2330&start=30&num=30
    for page in range(0, 3, 1):
        history_url = GOOGLE_FINANCE_HISTORY + CODE_TSMC + "&start=" + str(page * FINANCE_HISTORY_START_BASE) + "&num=" + str(FINANCE_HISTORY_RECORD_SIZE)
        finance_history_page = get_web_page(history_url, None)
        get_stock_history(finance_history_page)


if __name__ == '__main__':
    main()

