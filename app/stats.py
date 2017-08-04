"""
Helpers functions that allows to show different statistics
"""
from app.helpers import get_average_time, get_average_time_for_timedeltas


def get_stats(stores):
    luggagesTimes = []
    luggagesByDay = {}
    
    for el in stores:
        archiveTimeIn = el.get_proper_time_in()
        archiveTimeOut = el.get_proper_time_out()
        times = {
            'time': archiveTimeIn.time(),
            'in': archiveTimeIn.time().hour,
            'out': archiveTimeOut.time().hour if archiveTimeOut else None
        }
        if archiveTimeIn and archiveTimeOut:
            diff = (archiveTimeOut - archiveTimeIn)
            times['diff'] = diff
            luggagesTimes.append(diff)
        
        if luggagesByDay.has_key(archiveTimeIn.date()):
            luggagesByDay[archiveTimeIn.date()].append(times)
        else:
            luggagesByDay[archiveTimeIn.date()] = [times]
    
    stores = {}
    lenStores = []
    firstStores = []
    lastStores = []
    
    for key, value in luggagesByDay.iteritems():
        lenStores.append(len(value))
        hours = []
        hoursOut = []
        times = []
        diffs = []
        stores[key] = {'day': key, }
        for el in value:
            hours.append(el['in'])
            times.append(el['time'])
            if 'out' in el and el['out']:
                hoursOut.append(el['out'])
            if 'diff' in el and el['diff']:
                diffs.append(el['diff'])
        first = min(times)
        last = max(times)
        firstStores.append(first)
        lastStores.append(last)
        
        stores[key] = {'day': key, 'count': len(value), 'hours': hours, 'hoursOut': hoursOut,
                        'diff': get_average_time_for_timedeltas(diffs), 'first': first.strftime("%I:%M %p"), 'last': last.strftime("%I:%M %p") }
    
    count_store = int(round( sum(lenStores) / (len(lenStores) * 1.0) ) ) if (len(lenStores)) else 0
    
    return {
            'first_store': get_average_time(firstStores).strftime("%I:%M %p"),
            'last_store': get_average_time(lastStores).strftime("%I:%M %p"),
            'luggage_time': get_average_time_for_timedeltas(luggagesTimes),
            'count_store': count_store,
            'stores': stores
    }


