from favifind import celery, app
import time

@celery.task(name="test_task")
def test_task(seconds):
    print("Sleeping for {} seconds...".format(seconds))
    time.sleep(seconds)
    print("Done sleeping.")
