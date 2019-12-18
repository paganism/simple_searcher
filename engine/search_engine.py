from bs4 import BeautifulSoup
import requests
import lxml
import random
import argparse
import sys
sys.path.append('..')
from settings import HEADERS
import validators


def fetch_proxy_list():
    payload = {'anonymity': 'false', 'token': 'demo'}
    proxy_url = 'http://freeproxy-list.ru/api/proxy'
    proxy_list = requests.get(proxy_url, params=payload).text.split('\n')
    return proxy_list


def get_site_data(start_point, search_query=None, number=None):

    payload = {'q': search_query, 'num': number, 'numdoc': number}

    proxies = fetch_proxy_list()
    proxy = {"http": random.choice(proxies)} 

    if start_point.startswith('google') or start_point.startswith('yandex'):
        request = requests.get(f'https://{start_point}/search', params=payload, headers=HEADERS, proxies=proxy)
    else:
        request = requests.get(start_point)

    soup = BeautifulSoup(request.content, 'lxml')

    return soup


def validate_url(url):
    if validators.url(url):
        return True
    return False


def get_start_point_links_set(soup, start_point):

    links = set() 
    google_prefix = '/url?q='

    if start_point.startswith('google'):
        for tag_a in soup.find_all('a'):
            link = tag_a['href']

            if link.startswith(google_prefix):
                link = link[len(google_prefix):]
                if validate_url(link):
                    links.add(link)

    elif start_point.startswith('yandex'):
        for tag_a in soup.find_all('a', class_="link link_theme_normal organic__url link_cropped_no i-bem"):
            link = tag_a['href']
            if validate_url(link):
                    links.add(link)
            links.add(link)
    else:
        return

    return links


def print_inner_links(links):
    for link in links:
        site_data = get_site_data(link)
        print(f'START POINT LINK: {link}')
        for tag_a in site_data.find_all('a'):
            try:
                if validate_url(tag_a['href']):
                    print(f"INNER LINK: {tag_a['href']}")
            except KeyError:
                print('Do not contain a link')


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--search_query',
        dest='search_query',
        required=True,
        help='String which to search'
    )

    parser.add_argument(
        '--start_point',
        dest='start_point',
        required=True,
        help='Start point (google, yandex)'
    )

    parser.add_argument(
        '--number',
        dest='number',
        default=10,
        help='Number of results'
    )

    parser.add_argument(
        '--recursion',
        dest='recursion',
        default=0,
        help='Fetch inner links'
    )

    return parser.parse_args()
