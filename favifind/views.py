from favifind import app
from favifind.utils.database import query_favicon
from flask import render_template, request, redirect


@app.route('/')
def index():
    """
    Main and only view for FaviFind that displays a favicon
    to the user based on his/her query.

    Takes 'd' (domain) and 'fresh' query string parameters.
    """
    favicon = None
    domain = request.args.get('d')
    result = domain is not None
    if domain == "":
        return redirect('/')
    fresh = request.args.get('fresh')

    get_fresh = False
    if fresh:
        get_fresh = True

    if result:
        try:
            favicon = query_favicon(domain, get_fresh=get_fresh)
        except:
            # Don't throw an error, but return None
            pass
    return render_template('index.html', favicon=favicon, result=result)
