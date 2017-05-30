from bs4 import BeautifulSoup
import requests
import random

# TODO: This can be refactor as an router component.
if __name__ == '__main__':
    proxy_ips = ['114.25.211.38:7788', '114.25.211.38:30846']
    ip = random.choice(proxy_ips)
    print('Use', ip)
    resp = requests.get('http://whatismyip.org/', proxies={'http': 'http://' + ip})
    soup = BeautifulSoup(resp.text, 'html5lib')
    print(soup.find_all('div')[1].text.replace('\n', '').strip())
