from favifind import app
from favifind.utils.database import query_favicon
from flask import render_template, request


@app.route('/')
def index():
    """
    """
    favicon = None
    get_fresh = False

    domain = request.args.get('d')
    fresh = request.args.get('fresh')

    if fresh:
        get_fresh = True

    result = domain is not None
    if domain:
        favicon = query_favicon(domain, get_fresh=get_fresh)
    return render_template('index.html', favicon=favicon, result=result)
