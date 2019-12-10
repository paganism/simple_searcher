from bs4 import BeautifulSoup
import requests
import lxml
import random
import argparse


def fetch_proxy_list():
    payload = {'anonymity': 'false', 'token': 'demo'}
    proxy_url = 'http://freeproxy-list.ru/api/proxy'
    proxy_list = requests.get(proxy_url, params=payload).text.split('\n')
    return proxy_list


def get_site_data(start_point, search_query=None, number=None):
    headers = {
            'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:45.0) '
                'Mozilla/5.0 (Unknown; Linux) AppleWebKit/538.1 (KHTML, like Gecko) Chrome/v1.0.0 Safari/538.1'
                'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
        }

    payload = {'q': search_query, 'num': number, 'numdoc': number}

    proxies = fetch_proxy_list()
    proxy = {"http": random.choice(proxies)} 

    if start_point.startswith('google') or start_point.startswith('yandex'):
        request = requests.get(f'https://{start_point}/search', params=payload, headers=headers, proxies=proxy)
    else:
        request = requests.get(start_point)

    soup = BeautifulSoup(request.content, 'lxml')

    return soup

def get_start_point_links_set(soup, start_point):

    links = set() 
    google_prefix = '/url?q='

    if start_point.startswith('google'):
        for tag_a in soup.find_all('a'):
            link = tag_a['href']

            if link.startswith(google_prefix):
                link = link[len(google_prefix):]
                links.add(link)

    elif start_point.startswith('yandex'):
        for tag_a in soup.find_all('a', class_="link link_theme_normal organic__url link_cropped_no i-bem"):
            link = tag_a['href']
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
                print(f"INNER LINK: {tag_a['href']}")
            except KeyError:
                pass


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


if __name__ == '__main__':

    args = parse_arguments()
    
    site_data = get_site_data(args.start_point, args.search_query, args.number)
    start_point_links = get_start_point_links_set(site_data, args.start_point)

    if int(args.recursion) > 0:
        print_inner_links(start_point_links)

    else:
        for link in start_point_links:
            print(link)
