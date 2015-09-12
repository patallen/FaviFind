from favifind import db
from favifind.models import Favicon
from favifind.utils.favicons import resolve_url, get_favicon


def query_favicon(url, update=True):
    """
    Query the database for the favicon.
    If check_new is True, use get_favicon to update
    the database to reflect newest favicon.
    """
    # 1. Resolve the URL given
    rurl = resolve_url(url)
    # 2. Try to get the favicon in DB
    favicon = Favicon.query.filter_by(url=rurl).first()

    # If set to update, put the new favicon in DB and return it
    if update:
        f = get_favicon(rurl)
        if f:
            new_favicon = Favicon(url=rurl, favicon=f)
            db.session.add(new_favicon)
            db.session.commit()
            return new_favicon

    # If not set to update, return favicon in DB
    return favicon
