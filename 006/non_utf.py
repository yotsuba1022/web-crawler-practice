import requests
from bs4 import BeautifulSoup


def baidu_encoding():
    resp = requests.get('https://zhidao.baidu.com/question/48795122.html')
    resp.encoding = 'gbk'
    soup = BeautifulSoup(resp.text, 'html.parser')
    title = soup.find('span', 'ask-title').text.strip()
    content = soup.find('span', 'con').text.strip().replace('\n', '')
    print('title', title)
    print('content', content)
    try:
        with open(title + '.txt', 'w', encoding='UTF-8') as file:
            file.write(content)
    except Exception as e:
        print(e)


def gold_66_encoding():
    resp = requests.get('http://www.books.com.tw/activity/gold66_day/')
    resp.encoding = 'big5'
    soup = BeautifulSoup(resp.text, 'html.parser')
    books = list()
    for div in soup.find_all('div', 'sec_day'):
        books.append(div.h1.a.text + div.find_all('h2')[1].text + div.find_all('h2')[2].text)
    print('\n'.join(books))
    try:
        with open('66.txt', 'w', encoding='UTF-8') as file:
            file.write('\n'.join(books))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    baidu_encoding()
    gold_66_encoding()

