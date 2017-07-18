"""
Helpers functions that allows to show different statistics
"""
from app.helpers import get_average_time, get_average_time_for_timedeltas


def get_first_and_last_stores(stores):
    luggagesByDay = {}
    for el in stores:
        archiveTimeIn = el.get_proper_time_in()
        if luggagesByDay.has_key(archiveTimeIn.date()):
            luggagesByDay[archiveTimeIn.date()].append(archiveTimeIn.time())
        else:
            luggagesByDay[archiveTimeIn.date()] = [ archiveTimeIn.time() ]
    stores = {}
    firstStores = []
    lastStores = []
    
    for key, value in luggagesByDay.iteritems():
        first = min(value)
        last = max(value)
        firstStores.append(first)
        lastStores.append(last)
        stores[key] = {'day': key, 'first': first.strftime("%I:%M %p"), 'last': last.strftime("%I:%M %p")}
    
    return {
            'first_store': get_average_time(firstStores).strftime("%I:%M %p"),
            'last_store': get_average_time(lastStores).strftime("%I:%M %p"),
            'stores': stores
    }



def get_luggage_time(stores):
    luggagesTimes = []
    luggagesByDay = {}
    for el in stores:
        archiveTimeIn = el.get_proper_time_in()
        archiveTimeOut = el.get_proper_time_out()
        if archiveTimeIn and archiveTimeOut:
            diff = (archiveTimeOut - archiveTimeIn)
            luggagesTimes.append(diff)
            if luggagesByDay.has_key(archiveTimeIn.date()):
                luggagesByDay[archiveTimeIn.date()].append(diff)
            else:
                luggagesByDay[archiveTimeIn.date()] = [ diff ]
        
    stores = {}
    for key, value in luggagesByDay.iteritems():
        stores[key] = {'day': key, 'diff': get_average_time_for_timedeltas(value) }
    return {
            'luggage_time': get_average_time_for_timedeltas(luggagesTimes),
            'stores': stores
    }



def count_stores(stores):
    luggagesByDay = {}
    for el in stores:
        archiveTimeIn = el.get_proper_time_in()
        if luggagesByDay.has_key(archiveTimeIn.date()):
            luggagesByDay[archiveTimeIn.date()] += 1
        else:
            luggagesByDay[archiveTimeIn.date()] = 1
    stores = {}
    lenStores = []
    
    for key, value in luggagesByDay.iteritems():
        lenStores.append(value)
        stores[key] = {'day': key, 'count': value }
    
    return {
            'count_store': int(round( sum(lenStores) / (len(lenStores) * 1.0) ) ),
            'stores': stores
    }

def count_stores_by_hour(stores):
    luggagesByDay = {}
    for el in stores:
        archiveTimeIn = el.get_proper_time_in()
        if luggagesByDay.has_key(archiveTimeIn.strftime("%H")):
            luggagesByDay[archiveTimeIn.strftime("%H")] += 1
        else:
            luggagesByDay[archiveTimeIn.strftime("%H")] = 1
    stores = {}
    lenStores = []
    
    for key, value in luggagesByDay.iteritems():
        lenStores.append(value)
        stores[key] = {'hour': key, 'count': value }
    
    return {
            'count_store': int(round( sum(lenStores) / (len(lenStores) * 1.0) ) ),
            'stores': stores
    }

