import requests
from bs4 import BeautifulSoup


def main():
    url = 'http://blog.castman.net/web-crawler-tutorial/ch2/blog/blog.html'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    # The following two lines are the same.
    # print(soup.find('h4'))
    print('Content of the first h4:')
    print(soup.h4)

    # To find the first text content of anchor of h4
    print('\nText content of the first h4:')
    print(soup.h4.a.text)

    print('\nTo find all the h4 text content:')
    h4_tags = soup.find_all('h4')
    for h4 in h4_tags:
        print(h4.a.text)

    print('\nTo find all the h4 text content with class named \'card-title\' :')
    # The following three ways are the same.
    # h4_tags = soup.find_all('h4', {'class': 'card-title'})
    # h4_tags = soup.find_all('h4', 'card-title')
    h4_tags = soup.find_all('h4', class_='card-title')
    for h4 in h4_tags:
        print(h4.a.text)

    print('\nTo find elements with id attribute: ')
    print(soup.find(id='mac-p').text.strip())
    # If the attribute key contains special character, it will occur SyntaxError:
    # print(soup.find(data-foo='mac-p').text.strip())
    # To prevent this, you can do as the following line:
    print(soup.find_all('', {'data-foo': 'mac-foo'}))

    print('\nTo retrieve all the blog post\'s information:')
    divs = soup.find_all('div', 'content')
    for div in divs:
        # If we only use print(div.text) to retrieve the content, it's not easy to handle the information,
        # to make the retrieved data clearly, you can craw the blog page like this:
        print(div.h6.text.strip(), div.h4.a.text.strip(), div.p.text.strip())

    # There is also another good way the retrieve the blog info, by stripped_strings() function,
    # it will return all the text content that are under the parent tag, even wrap by other sub tags.
    # However, the return object of stripped_strings is an iterator object, so it's not human-readable.
    # To solve this, take a look at following code block:
    print('\nTo find all blog contents via stripped_strings function:')
    for div in divs:
        # If you feel it's hard to understand, google "[s for s in subsets(S)]"
        print([s for s in div.stripped_strings])


if __name__ == '__main__':
    main()