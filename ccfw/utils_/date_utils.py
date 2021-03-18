from datetime import datetime, timedelta

def date_range(start, stop, step = timedelta(1)):
    current = start
    while current < stop:
        yield current
        current += step
