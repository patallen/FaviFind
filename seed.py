from favifind.tasks import load_favicon
import csv


def load_urls(count=1000):
    """
    Loads the given number of urls from alexa.csv into the
    load_favicon task and places them in the Queue.
    """
    with open('alexa.csv') as alexa_csv:
        reader = csv.reader(alexa_csv, delimiter=',')
        for i, row in enumerate(reader, 1):
            if i <= count:
                load_favicon.delay(row[1])
                print("{}: {}".format(i, row[1]))


if __name__ == '__main__':
    print("Loading all URLs into Task Queue...")
    load_urls(200000)
