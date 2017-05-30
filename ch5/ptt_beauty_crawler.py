import requests
import time
from bs4 import BeautifulSoup
import os
import re
import urllib.request
import json


PTT_URL = 'https://www.ptt.cc'


def get_web_content(url):
    resp = requests.get(url=url, cookies={'over18': '1'})
    if resp.status_code != 200:
        print('Invalid url: ' + resp.url)
        return None
    else:
        return resp.text


def get_articles(dom, date):
    soup = BeautifulSoup(dom, 'html5lib')

    paging_dev = soup.find('div', 'btn-group btn-group-paging')
    prev_url = paging_dev.find_all('a')[1]['href']

    articles = []
    divs = soup.find_all('div', 'r-ent')
    for div in divs:
        if div.find('div', 'date').text.strip() == date:
            push_count = 0
            push_str = div.find('div', 'nrec').text
            if push_str:
                try:
                    push_count = int(push_str)
                except ValueError:
                    if push_str == '爆':
                        push_count = 99
                    elif push_str.startswith('X'):
                        push_count = -10

            if div.find('a'):
                href = div.find('a')['href']
                title = div.find('a').text
                author = div.find('div', 'author').text if div.find('div', 'author') else ''
                articles.append({
                    'title': title,
                    'href': href,
                    'push_count': push_count,
                    'author': author
                })
    return articles, prev_url


def parse(dom):
    soup = BeautifulSoup(dom, 'html.parser')
    links = soup.find(id='main-content').find_all('a')
    img_urls = []
    for link in links:
        if re.match(r'^https?://(i.)?(m.)?imgur.com', link['href']):
            img_urls.append(link['href'])
    return img_urls


def save(img_urls, title):
    if img_urls:
        try:
            folder_name = title.strip()
            os.makedirs(folder_name)
            for img_url in img_urls:
                # e.g. 'http://imgur.com/9487qqq.jpg'.split('//') -> ['http:', 'imgur.com/9487qqq.jpg']
                if img_url.split('//')[1].startswith('m.'):
                    img_url = img_url.replace('//m.', '//i.')
                if not img_url.split('//')[1].startswith('i.'):
                    img_url = img_url.split('//')[0] + '//i.' + img_url.split('//')[1]
                if not img_url.endswith('.jpg'):
                    img_url += '.jpg'
                file_name = img_url.split('/')[-1]
                urllib.request.urlretrieve(img_url, os.path.join(folder_name, file_name))
        except Exception as e:
            print(e)


def main():
    current_page = get_web_content(PTT_URL + '/bbs/Beauty/index.html')
    if current_page:
        articles = []
        date = time.strftime("%m/%d").lstrip('0')
        current_articles, prev_url = get_articles(current_page, date)
        while current_articles:
            articles += current_articles
            current_page = get_web_content(PTT_URL + prev_url)
            current_articles, prev_url = get_articles(current_page, date)

        for article in articles:
            print('Collecting beauty from:', article)
            page = get_web_content(PTT_URL + article['href'])
            if page:
                img_urls = parse(page)
                save(img_urls, article['title'])
                article['num_image'] = len(img_urls)

        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(articles, file, indent=2, sort_keys=True, ensure_ascii=False)


if __name__ == '__main__':
    main()

