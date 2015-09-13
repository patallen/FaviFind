from favifind import db
from favifind.models import Favicon
from favifind.utils.favicons import resolve_url, get_favicon




def query_favicon(url, get_fresh=True):
    """
    Query the database for the favicon.
    If get_fresh is True, use get_favicon to update
    the database to reflect newest favicon.
    """
    favicon = None

    # Try to resolve URL, otherwise return None
    rurl = resolve_url(url)

    # No matter what, we will need to check for existing favicon
    favicon = Favicon.query.filter_by(url=rurl).first()

    if get_fresh:
        # If get_fresh is true we will not even check the database
        f = get_favicon(rurl)
        if f:
            if favicon:
                favicon.favicon = f
            else:
                favicon = Favicon(url=rurl, favicon=f)
            db.session.add(favicon)
            db.session.commit()
        else:
            # Return None if couldn't get favicon
            # We do not want to return existing
            return None
    else:
        if not favicon:
            f = get_favicon(rurl)
            if f:
                favicon = Favicon(url=rurl, favicon=f)
                db.session.add(favicon)
                db.session.commit()

    return favicon
