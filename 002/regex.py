import requests
import re
from bs4 import BeautifulSoup


def main():
    url = 'http://blog.castman.net/web-crawler-tutorial/ch2/blog/blog.html'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    find_text_content_by_reg(soup, 'h[1-6]')

    # [a-zA-Z0-9]+ -> means that we hope the result string is composed by character a~z, A~Z and 0~9,
    # and the string length should ≥ 1 (which represented by "+").

    # http://[a-zA-Z0-9\.]+ -> means hyper link.

    # [\u4e00-\u9fa5]+ -> means all the chinese words in unicode format.

    print('\nFind all .png img source:')
    # To find png type image source by reg.
    # $ means the tail, the end of the string.
    # \. means ".", the \ is for escaping the special characters.
    png_source_pattern = '\.png$'
    find_img_source_by_reg(soup, png_source_pattern)

    # To find png type image source which contains "beginner" in source name by reg.
    # In the pattern, the "." after beginner means any words,
    # the * means the length is 0 or 1.
    print('\nFind all .png img sources that contain \"beginner\" in file name:')
    find_img_source_by_reg(soup, 'beginner.*'+png_source_pattern)

    print('\nTo count the blog number:')
    blog_class_pattern = 'card\-blog$'
    count_blog_number(soup, blog_class_pattern)

    print('\nTo find how many image sources contains the word \"crawler\"')
    target_pattern = 'crawler.*'
    find_img_source_by_reg(soup, target_pattern)

# re.compile API DOC: https://docs.python.org/3/library/re.html#re.compile
def find_text_content_by_reg(soup, reg_pattern):
    for element in soup.find_all(re.compile(reg_pattern)):
        print(element.text.strip())


def find_img_source_by_reg(soup, source_type):
    for img in soup.find_all('img', {'src': re.compile(source_type)}):
        print(img['src'])


def count_blog_number(soup, blog_pattern):
    count = len(soup.find_all('div', {'class': re.compile(blog_pattern)}))
    print('Blog count: ' + str(count))


if __name__ == '__main__':
    main()