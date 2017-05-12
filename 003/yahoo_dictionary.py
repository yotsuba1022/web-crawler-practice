import requests
from bs4 import BeautifulSoup
import urllib.parse


YAHOO_DICTIONARY_URL = "https://tw.dictionary.yahoo.com/dictionary?p="
YAHOO_REFERER_VALUE = "https://tw.dictionary.yahoo.com/dictionary"


def get_web_content(url, query):
    query = urllib.parse.quote_plus(query)
    resp = requests.get(url + query, headers={'Referer': YAHOO_REFERER_VALUE})
    if resp.status_code != 200:
        print('Invalid url: ', resp.url)
        return None
    else:
        return resp.text


def get_dict_info(dom):
    soup = BeautifulSoup(dom, 'html5lib')
    for explain in soup.find('ul', 'explanations').find_all('li', 'exp-item'):
        print(explain.text)


def main():
    page = get_web_content(YAHOO_DICTIONARY_URL, 'Java')
    if page:
        get_dict_info(page)


if __name__ == '__main__':
    main()
