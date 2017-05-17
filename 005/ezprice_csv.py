import requests
import urllib.parse
import csv
from bs4 import BeautifulSoup


EZPRICE_URL = 'https://ezprice.com.tw'
CSV_FILE_NAME = 'ezprice.csv'


def get_web_content(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        print('Invalid url: ' + resp.url)
        return None
    else:
        return resp.text


def get_price_info(query):
    encoded_query = urllib.parse.quote(query)
    url = EZPRICE_URL + '/s/%s/price/' % encoded_query
    result_page = get_web_content(url)
    dom = BeautifulSoup(result_page, 'html5lib')
    return dom


def extract_results(dom):
    items = list()
    for div in dom.find_all('div', 'search-rst clearfix'):
        item = list()
        item.append(div.h4.a['title'])
        item.append(div.find(itemprop='price')['content'])
        if div.find('span', 'platform-name'):
            item.append(div.find('span', 'platform-name').text.strip())
        else:
            item.append('N/A')
        items.append(item)
    print('Total items: %d.' % (len(items)))
    return items


def show_results(items):
    for item in items:
        print(item)


def write_to_csv_file(items):
    with open(CSV_FILE_NAME, 'w', encoding='UTF-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(('Item', 'Price', 'Store'))
        for item in items:
            writer.writerow((column for column in item))


def read_from_csv_file():
    print('\nRead from csv file: ' + CSV_FILE_NAME)
    with open(CSV_FILE_NAME, 'r', encoding='UTF-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row['Item'], row['Price'], row['Store'])


def main():
    query = '吉胖喵'
    dom = get_price_info(query)
    items = extract_results(dom)
    show_results(items)
    write_to_csv_file(items)
    read_from_csv_file()


if __name__ == '__main__':
    main()

