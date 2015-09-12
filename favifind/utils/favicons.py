import csv
import requests
from urlparse import urlparse, urljoin
from bs4 import BeautifulSoup as bs


TIMEOUT = 2


def resolve_url(url):
    """
    Takes a url and returns the result after
    following redirects
    """
    try:
        with requests.Session() as s:
            s.max_redirects = 30
            # Use .get - .head doesn't always resolve properly
            res = s.get(base_url(url), timeout=TIMEOUT, allow_redirects=True)
            return res.url
    except:
        return None


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


def get_favicon(resolved_url):
    """
    Takes a resolved url and returns it's favicon
    """
    # First, check if base_url returns OK with '/favicon.ico'
    favicon_url = base_url(resolved_url) + 'favicon.ico'
    user_agent = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(favicon_url, timeout=TIMEOUT,
                           headers=user_agent, allow_redirects=True)
    except Exception:
        return None
    if res.status_code == 200:
        return res.url
    else:
        # If we can't resolve '/favicon.ico', try to use
        # BeautifulSoup to get the 'shortcut icon' link
        try:
            res = requests.get(base_url(resolved_url), timeout=TIMEOUT)
            soup = bs(res.content, "html.parser")
            icon_link = soup.find('link', rel="shortcut icon")
            icon = icon_link['href']
            return urljoin(res.url, icon)
        except Exception:
            pass
    return None


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
                if favicon == "":
                    err_count += 1
                print("{}: {}".format(i, favicon))
        summary = "\nSummary:\n--------\nUnknown: {}\nPct Unknown: {}"
        print(summary.format(err_count, (err_count*1.0)/count*100))
