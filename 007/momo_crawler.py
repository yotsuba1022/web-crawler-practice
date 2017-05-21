import urllib.parse
import requests
import time
import json
import os
from bs4 import BeautifulSoup


STORE = 'momo'
MOMO_MOBILE_URL = 'http://m.momoshop.com.tw/'
MOMO_QUERY_URL = MOMO_MOBILE_URL + 'mosearch/%s.html'
USER_AGENT_VALUE = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'


def get_web_content(query):
    encoded_query = urllib.parse.quote(query)
    query_url = MOMO_QUERY_URL % encoded_query
    headers = {'User-Agent': USER_AGENT_VALUE}
    resp = requests.get(query_url, headers=headers)
    if not resp:
        return []
    resp.encoding = 'UTF-8'
    return BeautifulSoup(resp.text, 'html.parser')


def search_momo(query):
    dom = get_web_content(query)
    if dom:
        items = []
        for element in dom.find(id='itemizedStyle').ul.find_all('li'):
            item_name = element.find('p', 'prdName').text
            item_price = element.find('b', 'price').text.replace(',', '')
            if not item_price:
                continue
            item_price = int(item_price)
            item_url = MOMO_MOBILE_URL + element.find('a')['href']
            item_img_url = element.a.img['src']

            item = {
                'name': item_name,
                'price': item_price,
                'url': item_url,
                'img_url': item_img_url
            }

            items.append(item)
        return items


def save_search_result(data):
    with open(os.path.join('json', data['date'] + '-%s.json' % STORE), 'w', encoding='UTF-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def main():
    query_str = 'iPhone 7 Plus 128G'
    items = search_momo(query_str)
    today = time.strftime('%m-%d')
    print('Search item \'%s\' from %s...' % (query_str, STORE))
    print('Search %d records on %s' % (len(items), today))
    for item in items:
        print(item)
    data = {
        'date': today,
        'store': STORE,
        'items': items
    }

    save_search_result(data)


if __name__ == '__main__':
    main()
