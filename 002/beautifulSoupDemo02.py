import requests
from bs4 import BeautifulSoup

# Structure of the example html page:
#  body
#   - div
#     - h2
#     - p
#     - table.table
#       - thead
#         - tr
#           - th
#           - th
#           - th
#           - th
#       - tbody
#         - tr
#           - td
#           - td
#           - td
#           - td
#             - a
#               - img
#         - tr
#         - ...


def main():
    url = 'http://blog.castman.net/web-crawler-tutorial/ch2/table/table.html'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    calculate_course_average_price1(soup)
    calculate_course_average_price2(soup)
    retrieve_all_tr_contents(soup)


def calculate_course_average_price1(soup):
    # To calculate the average course price
    # Retrieve the record with index:
    prices = []
    rows = soup.find('table', 'table').tbody.find_all('tr')
    for row in rows:
        price = row.find_all('td')[2].text
        print(price)
        prices.append(int(price))
    print('Average course price: ' + str(sum(prices) / len(prices)) + '\n')


def calculate_course_average_price2(soup):
    # Retrieve the record via siblings:
    prices = []
    links = soup.find_all('a')
    for link in links:
        price = link.parent.previous_sibling.text
        prices.append(int(price))
    print('Average course price: ' + str(sum(prices) / len(prices)) + '\n')


def retrieve_all_tr_contents(soup):
    # Retrieve all tr record:
    rows = soup.find('table', 'table').tbody.find_all('tr')
    for row in rows:
        # Except all_tds = row.find_all('td'), you can also retrieve all td record with the following line code:
        all_tds = [td for td in row.children]
        if 'href' in all_tds[3].a.attrs:
            href = all_tds[3].a['href']
        else:
            href = None
        print(all_tds[0].text, all_tds[1].text, all_tds[2].text, href, all_tds[3].a.img['src'])


if __name__ == '__main__':
    main()