import requests
from bs4 import BeautifulSoup


GOOGLE_FINANCE_INFO = "https://www.google.com/finance?q="
GOOGLE_FINANCE_HISTORY = "https://www.google.com/finance/historical?q="
CODE_TSMC = "TPE:2330"


def get_web_page(url, query):
    resp = requests.get(url+query)
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

    finance_history_page = get_web_page(GOOGLE_FINANCE_HISTORY, CODE_TSMC)
    get_stock_history(finance_history_page)


if __name__ == '__main__':
    main()

