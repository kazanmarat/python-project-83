from urllib.parse import urlparse
import validators


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
