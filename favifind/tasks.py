from favifind import celery
from favifind.utils import database
import time


@celery.task(name="test_task")
def test_task(seconds):
    print("Sleeping for {} seconds...".format(seconds))
    time.sleep(seconds)
    print("Done sleeping.")


@celery.task(name="load_favicon", max_retries=3)
def load_favicon(url):
    """
    Function to be used by celery that takes a URL
    and passes it to the query_favicon function.
    """
    return database.query_favicon(url)
