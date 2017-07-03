"""
Helpers functions that allows to show different statistics
"""
from app.helpers import get_average_time


def get_first_and_last_stores(stores):
    luggagesByDay = {}
    for el in stores:
        archiveTimeIn = el.get_proper_time_in()
        if luggagesByDay.has_key(archiveTimeIn.date()):
            luggagesByDay[archiveTimeIn.date()].append(archiveTimeIn.time())
        else:
            luggagesByDay[archiveTimeIn.date()] = [ archiveTimeIn.time() ]
    firstStores = []
    lastStores = []
    
    for value in luggagesByDay.itervalues():
        firstStores.append( min(value) )
        lastStores.append( max(value) )
    
    return {
            'first_store': get_average_time(firstStores),
            'last_store': get_average_time(lastStores)
    }

