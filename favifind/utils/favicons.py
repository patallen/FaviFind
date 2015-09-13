import re
import csv
import requests
from urlparse import urlparse, urljoin
from bs4 import BeautifulSoup as bs


class ResolveException(BaseException):
    pass


class GetFaviconException(BaseException):
    pass


TIMEOUT = 5

user_agent = {'User-Agent': ''}
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
        with requests.Session() as s:
            s.max_redirects = 30
            # Use .get - .head doesn't always resolve properly
            res = s.get(base_url(url), **rkwargs)
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
        try:
            res = requests.get(base_url(res_url), **rkwargs)
            soup = bs(res.content, "html.parser")
            icon_link = soup.find('link', rel=re.compile('icon', re.I))
            icon = icon_link['href']
            return urljoin(res.url, icon)
        except:
            raise GetFaviconException("Unable to get favicon for {}".format(res_url))


def print_csv(count=1000):
    """
    Used for DEBUG purposes, this function loops
    through the CSV *count* number of times and prints
    to the console with a final summary.
    """
    with open('alexa.csv') as alexa_csv:
        reader = csv.reader(alexa_csv, delimiter=',')
        err_count = 0
        for i, row in enumerate(reader, 1):
            if i <= count:
                favicon = get_favicon(row[1])
                if favicon is None:
                    err_count += 1
                print("{}: {}".format(i, favicon))
        summary = "\nSummary:\n--------\nUnknown: {}\nPct Unknown: {}"
        print(summary.format(err_count, (err_count*1.0)/count*100))
