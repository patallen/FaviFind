from favifind import celery
from favifind.utils import database
import time
import csv


@celery.task(name="test_task")
def test_task(seconds):
    print("Sleeping for {} seconds...".format(seconds))
    time.sleep(seconds)
    print("Done sleeping.")


@celery.task(name="load_favicon", max_retries=3)
def load_favicon(url):
    return database.query_favicon(url)


def do_all(count=1000):
    # favicons from alexa.csv
    with open('alexa.csv') as alexa_csv:
        reader = csv.reader(alexa_csv, delimiter=',')
        for i, row in enumerate(reader, 1):
            if i <= count:
                load_favicon.delay(row[1])
                print("{}: {}".format(i, row[1]))
