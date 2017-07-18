import config
from datetime import datetime, time, timedelta
import json
import string
import os
import functools
from flask import url_for as orig_url_for
import numbers

def currentyear():
    return datetime.now().year


def locations(selected_locations):
    try:
        selected_locations = json.loads(selected_locations) if selected_locations else dict()
    except ValueError, e:
        return selected_locations if selected_locations else ''

    if isinstance(selected_locations, numbers.Integral):
        return str(selected_locations)

    locations_filtered = {key: value for key, value in selected_locations.iteritems() if value}
    keys = []

    if locations_filtered:
        keys = locations_filtered.keys()
        keys.sort(key=string.lower)

    return ' '.join(keys)


def is_production():
    return config.PRODUCTION in os.getenv('FLAKS_CONFIGURATION', '')


def url_for(*args, **kwargs):
    if is_production():
        kwargs['_scheme'] = 'https'
        kwargs['_external'] = True

    return orig_url_for(*args, **kwargs)


def get_average_time(datetimes):
    total = sum(dt.hour * 3600 + dt.minute * 60 + dt.second for dt in datetimes)
    avg = total / len(datetimes) if (len(datetimes)) else 0
    minutes, seconds = divmod(int(avg), 60)
    hours, minutes = divmod(minutes, 60)
    return time(hours, minutes, seconds)


def get_average_time_for_timedeltas(timedeltas):
    if (len(timedeltas)):
        avg = sum(timedeltas, timedelta(0)) / len(timedeltas)
        avg = avg - timedelta(microseconds=avg.microseconds)
        return strfdelta(avg, "{days} days, {hours} hours, {minutes} minutes")
    else:
        return 0
    


def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

