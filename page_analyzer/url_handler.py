from urllib.parse import urlparse
import validators
import requests
from bs4 import BeautifulSoup


class URLValidationErrors(Exception):
    pass


class URLNotValid(URLValidationErrors):
    pass


class URLTooLong(URLValidationErrors):
    pass


def check_url(url):
    MAX_LENGTH_URL = 255
    if len(url) > MAX_LENGTH_URL:
        raise URLTooLong()
    if not validators.url(url):
        raise URLNotValid()


def clear_url(url):
    parse_url = urlparse(url)
    return f'{parse_url.scheme}://{parse_url.netloc}'


def get_content(url):
    TIME_ANSWER = 10
    response = requests.get(url, timeout=TIME_ANSWER)
    requests.Response.raise_for_status(response)
    status_code = response.status_code
    soup = BeautifulSoup(response.content, "html.parser")

    h1 = soup.find('h1').text if soup.find('h1') else ''
    title = soup.find('title').text if soup.find('title') else ''
    meta_description = soup.find('meta', {'name': "description"})
    description = meta_description["content"] if meta_description else ''
    return {'status_code': status_code,
            'h1': h1,
            'title': title,
            'description': description}
