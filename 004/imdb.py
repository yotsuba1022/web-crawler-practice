import requests
import json
import math
from collections import Counter


OMDB_URL = 'http://www.omdbapi.com'


def get_movie_date(url):
    data = json.loads(requests.get(url).text)
    if data['Response'] == 'True':
        return data
    else:
        return None


def search_ids_by_keyword(keywords):
    movie_ids = list()
    # e.g., "Iron Man" -> Iron+Man
    query = '+'.join(keywords.split())
    url = OMDB_URL + '/?s=' + query
    data = get_movie_date(url)

    if data:
        for item in data['Search']:
            movie_ids.append(item['imdbID'])
        total = int(data['totalResults'])
        num_pages = math.floor(total/10) + 1

        for i in range(2, num_pages+1):
            url = OMDB_URL + '/?s=' + query + '&page=' + str(i)
            data = get_movie_date(url)
            if data:
                for item in data['Search']:
                    movie_ids.append(item['imdbID'])
    return movie_ids


def search_by_id(movie_id):
    url = OMDB_URL + '/?i=' + movie_id
    data = get_movie_date(url)
    return data if data else None


def main():
    keyword = 'iron man'
    m_ids = search_ids_by_keyword(keyword)
    print('There are %s movies contain the keyword %s.' % (len(m_ids), keyword))
    print('Retrieving movie data...')
    movies = list()
    for m_id in m_ids:
        movies.append(search_by_id(m_id))
    print('Top 5 movie results:')
    for movie in movies[:5]:
        print(movie)
    years = [movie['Year'] for movie in movies]
    year_dist = Counter(years)
    print('Publish year distribution: ', year_dist)
    ratings = [float(movie['imdbRating']) for movie in movies if movie['imdbRating'] != 'N/A']
    print('Average rating: %.2f' % (sum(ratings)/len(ratings)))


if __name__ == '__main__':
    main()
