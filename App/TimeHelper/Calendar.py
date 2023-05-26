import Event
import TAGS
import dates
import json
class calendar:

    def __init__(self):
        self.dates = {

        }

    def add_event(self, event):
        date = event.date
        time = event.time

        if not(date in self.dates):
            self.dates[date] = dict()

        if time in self.dates[date]:
            if self.colision():
                self.dates[date][time] = dict()
        else:
            self.dates[date][time] = dict()

        self.dates[date][time][event.name] = event

#Напоминалки до и после

#оценка по умолчанию (только да или нет) (пример - работа) если статитика какое-то время была одинакова + рабочий тег

    def colision(self):
        '''Возвращает True, если решено сделать замену'''
        #todo Нужно подвязать к интерфейса (кидать рекомендацию)
        return False#bool(input("На эту дату уже есть событие, заменить? "))

    def remove_event(self,date,time,name):
        if name in self.dates[date][time]:
            del self.dates[date][time][name]
            if len(self.dates[date][time])== 0:
                del self.dates[date][time]
                if len(self.dates[date])==0:
                    del self.dates[date]

    def edit_event(self,date,time,name, changes):
        if name in self.dates[date][time]:
            ndate,ntime,ndesc = changes
            self.dates[date][time][name].edit(ndate,ntime,ndesc)
            self.add_event(self.dates[date][time][name])
            self.remove_event(date,time,name)

    def save(self):
        savedata = {}
        for i, date in enumerate(self.dates):
            savedata[date] = {}
            for time in self.dates[date]:
                savedata[date][time] = {}
                for event in self.dates[date][time]:
                    savedata[date][time][event]= self.dates[date][time][event].descripton

        with open("calendare.json", "w") as file:
            json.dump(savedata, file)
        file.close()

    def load(self):
        loaddata = None
        try:
            with open("calendare.json", "r") as file:
                loaddata = json.load(file)
            file.close()

            for date in loaddata:
                self.dates[date] = {}
                for time in loaddata[date]:
                    self.dates[date][time] = {}
                    for event in loaddata[date][time]:
                        e = Event.event(date,time,loaddata[date][time][event])
                        self.dates[date][time][event] = e

            self.sort()

            return True
        except Exception as e:
            print(e)
            return False

    def sort(self):
        for date in self.dates:
            self.dates[date] = dict(sorted(self.dates[date].items(), key = lambda x: x[0]))

    def get_period(self, start, end):
        period = []
        for i in dates.drange(start,end):
            key = i.strftime("%d.%m.%Y")
            if key in self.dates.keys():
                period.append(self.dates[key])
                print(f"{key}: {self.dates[key]}")
            else:
                period.append(list())
        return period

    def format(self, data):
        #print("tags")
        result = [None]*((1440*7)//45)
        for l,day in enumerate(data):
            tm = (l * 1441)
            for time in day:
                i = 0
                names = list(day[time].keys())
                print(F"___{day} {time} {names}")
                for t in range(0,1441,45):
                    name = names[i]
                    #print(f"t: {t}")
                    #print(f"event: {day[time][name].description['time']}, {name}")
                    if day[time][name].description["time"]>=t and day[time][name].description["time"]<t+45:
                        event = list(set(day[time][name].description).difference(TAGS.WTAGS))
                        result[(tm+t) // 45] = event
                        d = int(day[time][name].description["duration"])
                        k = 0
                        while d>45:
                            d -= 45
                            k += 1
                            if result[((tm+t) // 45)+k] is list:
                                result[((tm+t) // 45)+k]+event
                            else:
                                result[((tm+t) // 45) + k] = event
                        i += 1
                        #todo next day
                        if i==len(names):
                            break

        return result



