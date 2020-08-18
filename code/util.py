import datetime

def getTodayDateString():
    curDatetime = datetime.datetime.now()
    curDateString = curDatetime.strftime('%Y-%m-%d')
    return curDateString