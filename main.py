import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import argparse

def shorten_link(headers, user_url):
    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    long_url = {'long_url': user_url}
    response = requests.post(url, headers=headers, json=long_url)
    response.raise_for_status()
    return response.json()['link']


def count_clicks(headers, user_url):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{user_url}/clicks/summary'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(headers, user_url):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{user_url}'
    response = requests.get(url, headers=headers)
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser(
        description='Программа сокращает ссылки'
    )
    parser.add_argument('url', help='Ваша ссылка')
    args = parser.parse_args()
    headers = {'Authorization': f'Bearer {os.getenv("BITLY_TOKEN")}'}
    parsed_url = urlparse(args.url)
    no_scheme_url = f'{parsed_url.netloc}{parsed_url.path}'

    if is_bitlink(headers, no_scheme_url):
        try:
            print(f'Кол-во кликов: {count_clicks(headers, no_scheme_url)}')
        except requests.exceptions.HTTPError:
            print('Ошибка при подсчете кликов')
    else:
        try:
            print(f'Битлинк: {shorten_link(headers, args.url)}')
        except requests.exceptions.HTTPError:
            print('Ошибка при сокращении ссылки')
