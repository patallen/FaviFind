import csv
import urllib2


def normalize_url(url):
    """
    Adds 'http://' and trailing slash to url
    if they do not exist
    """
    if not url.startswith('http://'):
        url = url = 'http://' + url
    if not url.endswith('/'):
        url += '/'
    return url

def get_redirect_url(url):
    """
    Returns a url after following redirects
    """
    redirect_url = ''
    try:
        redirect_url = urllib2.urlopen(url, timeout=1).geturl()
    except:
        pass
    return redirect_url

def get_favicon(url):
    url = normalize_url(url)
    redirect_url = get_redirect_url(url)

    favicon_url = ''
    try:
        res = urllib2.urlopen(url + 'favicon.ico', timeout=1)
        favicon_url = res.geturl()
    except:
        pass
    # TODO: If the favicon_url does not end with '.ico'
    # Attempt to find in homepage HTML with BeautifulSoup
    if not favicon_url.endswith('.ico'):
        favicon_url = ""
    return favicon_url


if __name__ == '__main__':
    # For now, calling alexa.py will attempt to list out
    # favicons from alexa.csv
    with open('alexa.csv') as alexa_csv:
        reader = csv.reader(alexa_csv, delimiter=',')
        for i, row in enumerate(reader, 1):
            if i < 200:
                #print(row[1])
                print("{}: {}".format(i, get_favicon(row[1])))