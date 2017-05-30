import html
import urllib.parse
import time
import json
import requests
import os
from requests.adapters import HTTPAdapter


STORE = 'pchome'
SESSION_TIMEOUT = 3
SESSION_MAX_RETRIES = 3
PCHOME_API_ENDPOINT = 'http://ecshweb.pchome.com.tw/search/v3.3/all/results?q=%s&sort=rnk&price=%s-%s'
PCHOME_PRODUCT_URL_PREFIX = 'http://24h.pchome.com.tw/prod/'
PCHOME_IMG_URL_PREFIX = 'http://ec1img.pchome.com.tw/'


def get_web_content(query_url):
    session = requests.Session()
    session.mount(query_url, HTTPAdapter(max_retries=SESSION_MAX_RETRIES))
    try:
        # The timeout unit is second.
        resp = session.get(query_url, timeout=SESSION_TIMEOUT)
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    return resp


def collect_items(raw_data):
    extracted_items = list()
    raw_items = raw_data['prods']
    for raw_item in raw_items:
        try:
            item = dict()
            item['name'] = html.unescape(raw_item['name'])
            item['price'] = int(raw_item['price'])
            item['describe'] = raw_item['describe']
            item['img_url'] = PCHOME_IMG_URL_PREFIX + raw_item['picB']
            item['url'] = PCHOME_PRODUCT_URL_PREFIX + raw_item['Id']
            extracted_items.append(item)
        except Exception:
            pass
    return extracted_items


def search_pchome(query, min_price, max_price):
    query = urllib.parse.quote(query)
    query_url = PCHOME_API_ENDPOINT % (query, str(min_price), str(max_price))
    resp = get_web_content(query_url)
    if not resp:
        return []

    resp.encoding = 'UTF-8'
    data = resp.json()
    if data['prods'] is None:
        return []

    total_page_count = int(data['totalPage'])
    if total_page_count == 1:
        return collect_items(data)

    urls = []
    current_page = 1
    while current_page <= total_page_count:
        current_page_url = query_url + '&page=' + str(current_page)
        urls.append(current_page_url)
        current_page += 1

    items = []
    for url in urls:
        resp = get_web_content(url)
        if resp:
            resp.encoding = 'UTF-8'
            items += collect_items(resp.json())
    return items


def save_search_result(data):
    with open(os.path.join('json', data['date'] + '-%s.json' % STORE), 'w', encoding='UTF-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def main():
    query_str = 'iphone 7 128g plus'
    min_price = 20000
    max_price = 40000
    items = search_pchome(query_str, min_price, max_price)
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

