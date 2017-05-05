import requests
from bs4 import BeautifulSoup


def main():
    url = 'http://blog.castman.net/web-crawler-tutorial/ch1/connect.html'

    h1 = get_header_text(url, 'h1')
    if h1:
        print('h1: ' + h1)

    h2 = get_header_text(url, 'h2')
    if h2:
        print('h2: ' + h2)

    p = get_header_text(url, 'p')
    if p:
        print('p: ' + p)


def get_header_text(url, header_tag):
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            return soup.find(header_tag).text
    except Exception as exception:
        return None
    

if __name__ == '__main__':
    main()