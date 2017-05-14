import requests


ACCESS_TOKEN = ''


def get_my_friends():
    url = 'https://graph.facebook.com/v2.9/me?fields=id,name,friends&access_token={}'.format(ACCESS_TOKEN)
    data = requests.get(url).json()
    print('My ID: ' + data['id'])
    print('My name: ' + data['name'])
    print('Total friends: ', data['friends']['summary']['total_count'], 'friends.')


def get_page_post(page_id):
    url = 'https://graph.facebook.com/v2.9/{0}/posts?access_token={1}'.format(page_id, ACCESS_TOKEN)
    data = requests.get(url).json()
    print('There are ', len(data['data']), ' posts on the fans page.')
    print('The latest post time is: ', data['data'][0]['created_time'])
    print('Content:', data['data'][0]['message'])


def main():
    get_my_friends()
    get_page_post(1707015819625206)


if __name__ == '__main__':
    main()

