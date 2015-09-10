import csv
import urllib2
from bs4 import BeautifulSoup

def normalize_url(url):
    """
    Adds 'http://' and trailing slash to url
    if they do not exist
    """
    if not url.startswith('http://'):
        url = url = 'http://' + url
    if not url.endswith('/'):
        url += '/'
    print(url)
    return url

def bs_favicon(url):
    try:
        soup = BeautifulSoup(urllib2.urlopen(url).read(), "lxml")
        icon_link = soup.find('link', rel="shortcut icon")
        icon = icon_link['href']

        return icon
    except:
        pass


def get_redirect_url(url):
    """
    Returns a url after following redirects
    """
    redirect_url = ''
    try:
        redirect_url = urllib2.urlopen(url, timeout=2).geturl()
    except:
        pass
    return redirect_url

def get_favicon(url):
    url = normalize_url(url)
    redirect_url = get_redirect_url(url)

    favicon_url = ''
    try:
        favicon_url = urllib2.urlopen(url + 'favicon.ico', timeout=5).geturl()
    except:
        pass
    # TODO: If the favicon_url does not end with '.ico'
    # Attempt to find in homepage HTML with BeautifulSoup

    if not favicon_url.endswith('.ico'):
        try:
            favicon_url = bs_favicon(url)
        except:
            pass
    return favicon_url


if __name__ == '__main__':
    # For now, calling alexa.py will attempt to list out
    # favicons from alexa.csv
    with open('alexa.csv') as alexa_csv:
        reader = csv.reader(alexa_csv, delimiter=',')
        for i, row in enumerate(reader, 1):
            if i <= 100:
                #print(row[1])
                print("{}: {} \t\t{}".format(i, row[1], get_favicon(row[1])))