import datetime as dt

def drange(start, stop):#(d, m, y)
    res = []
    # d, m, y = start
    begin = dt.datetime(start.year, start.month, start.day)
    #d, m, y = stop
    end = dt.datetime(stop.year, stop.month, stop.day)
    while begin != end:
        res.append(begin)
        begin += dt.timedelta(1)
    res.append(end)
    return res

def days():
    wdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пяница", "Суббота", "Восресение"]
    today = dt.datetime.today()
    res = []
    for i in range(-3,4):
        day = today + dt.timedelta(i)
        res.append(f"{wdays[day.weekday()]}: {day.strftime('%d.%m.%Y')} ")
    return res

def today_range():
    today = dt.datetime.today()
    start = today + dt.timedelta(-3)
    stop = today + dt.timedelta(3)
    return (start, stop)