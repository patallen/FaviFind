from bs4 import BeautifulSoup as bs
from urlparse import urlparse, urljoin
import csv
import re
import requests


class ResolveException(Exception):
    pass


class GetFaviconException(Exception):
    pass


user_agent = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
# Timeout in seconds for requests methods
TIMEOUT = 3
# Used for keyword arguments in requests functions
rkwargs = {'timeout': TIMEOUT,
           'allow_redirects': True,
           'headers': user_agent,
           'verify': False}


def resolve_url(url):
    """
    Takes a url and returns the result after
    following redirects
    """
    try:
        # Use .get - .head doesn't always resolve properly
        res = requests.get(base_url(url), **rkwargs)
        return res.url
    except:
        raise ResolveException('Unable to resolve URL {}'.format(url))


def base_url(url):
    """
    Takes a url, checks that the url has a scheme, then returns
    the url base. EX: 'google.com' -> 'http://google.com/'
    """
    p = urlparse(url)
    if p.scheme == '':
        url = 'http://{}'.format(url)
    parsed_url = urlparse(url)
    return '{url.scheme}://{url.netloc}/'.format(url=parsed_url)


def get_favicon(res_url):
    """
    Takes a resolved url and returns it's favicon
    """
    # First, check if base_url returns OK with '/favicon.ico'
    favicon_url = base_url(res_url) + 'favicon.ico'
    try:
        res = requests.get(favicon_url, **rkwargs)
    except:
        raise GetFaviconException("No response from {}".format(favicon_url))

    if res.status_code == 200:
        return res.url
    else:
        # If we can't resolve '/favicon.ico', try to use
        # BeautifulSoup to get the 'icon' link
        # NOTE: This step should probably be done before trying to
        # resolve /favicon.ico because the link takes precidence.
        try:
            res = requests.get(base_url(res_url), **rkwargs)
            soup = bs(res.content, "html.parser")
            icon_link = soup.find('link', rel=re.compile('icon', re.I))
            icon = icon_link['href']
            return urljoin(res.url, icon)
        except:
            raise GetFaviconException("Unable to get favicon for {}"
                                      .format(res_url))
