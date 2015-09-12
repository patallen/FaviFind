from favifind import app
from favifind.utils.database import query_favicon
from flask import render_template, request


@app.route('/')
def index():
    favicon = None
    domain = request.args.get('d')
    result = domain is not None
    if domain:
        favicon = query_favicon(domain)
    return render_template('index.html', favicon=favicon, result=result)
