## FaviFind
[Live Version](http://107.191.41.253/) - Hosted on [Vultr.com](http://vultr.com/) VPS using nginx and uwsgi.

Web application for retrieving the favicon of a given website.


## Notes

If I had more time on this I would:

1. Continue to work on getting a lower % error rate on get_favicon. Not all favicons are coming back that should. During seeding, around 15% of requests come back without a favicon. Some of these are pages that are unavailable or do not have favicons, but the others can be found in-browser. A good estimate would be around 90% success rate.
 

1. Add a better UI:
  - Check validity of user input
  - Flash messages for errors
  - AJAX for the favicon instead of reloading page (display 'loading...' while user waits)


## Setup

#### Install
- `sudo apt-get install redis-server postgresql libpq-dev`

#### Environment
- `$ git clone http://github.com/patallen/favifind && cd favifind`
- `$ mkvritualenv favifind`
- `$ pip install -r requirements.txt`
- `$ python manage.py db upgrade`

#### Seed the database

The length of time that it will take to seed the database is dependent on the amount of RAM and number of cores on the machine.
For me, it took ~2-3 hours on 8GB RAM, 4 core VPS running 20 celery workers to try to retrieve and seed 200,000 favicon URLs.
- Launch workers with celery multi:
	- `$ celery multi 20 -A favifind.celery`
- Start up Flower for monitoring
	- `$ celery flower -A favifind.celery --port=5000`
- Finally, `$ python seed.py`, and monitor in-browser from port 5000.
