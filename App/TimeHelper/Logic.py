import Event
from Calendar import *
from Brain import *
from ExpBank import *
import datetime as dt
import TAGS
from client import p2pnet
import Profile
import time

class Logic():

    def __init__(self):
        self.prof = Profile.prof()
        self.Key = self.prof.key()

        self.C = calendar()
        self.Bank = ExpBank()
        self.optimazer = Adam(learning_rate=0.01)
        self.Brain = Agent(self.C, self.optimazer, self.Bank, self.Key)
        self.Brain._build_compile_model()

        self.needrate = {}
        self.load()

        self.LastForm = None

        try:
            self.C.load()
        except:
            self.C.save()

    def loadprofile(self):
        return self.prof.load()

    def get_day(self, day):
        print(self.C.dates)
        print(day)
        try:
            events = []
            D = self.C.dates[day]
            for time in D:
                for name in D[time]:
                    tags = list(set(D[time][name].description).difference(TAGS.WTAGS))
                    events.append([time, name, tags])

            return events

        except Exception as e:
            print(e)
            return None

    def save(self):
        with open("needrate.json", "w") as file:
            json.dump(self.needrate, file)
        file.close()

    def load(self):
        try:
            with open("needrate.json", "r") as file:
                self.needrate = json.load(file)
            file.close()
        except Exception as e:
            print(e)

    def recomendation(self, event):
        tdr = dates.today_range()
        print(tdr)
        state = self.C.format(self.C.get_period(tdr[0], tdr[1]))
        print(state)
        state = state + [event]
        print(state)
        action,expid = self.Brain.act(state)
        today = dt.datetime.today()
        date = today + dt.timedelta(action+1)
        self.needrate[date.strftime('%d.%m.%Y')] = expid
        self.save()
        print(date)
        #self.Brain.balans_action(state)
        #self.rate(expid,0.5)
        return date


    def rate(self,expid,rate):
        self.Brain.retrain(expid,rate)

    def addevent(self, date, time, descript):
        print(date, time, descript)
        event = Event.event(date = date, time = time, description = descript)
        self.C.add_event(event)
        self.C.sort()
        self.C.save()

    def update_data(self):
        net = p2pnet(f"client{self.Key}")#todo google id?
        net.send({"command": "down"})

    def get_skills(self):
        return self.prof.skills

    def get_needrate(self):
        return self.needrate

    def set_LastForm(self,data):
        self.LastForm = data

    def use_LastForm(self,Path):
        match Path:
            case "Skills":
                self.prof.set_skills(self.LastForm)
                self.prof.save()


# Что хоти видеть в профиле? - skills mbti name
# Нужны ли настройки? Какие? цвета
# На что завизать опросы - кнопочка оценка рекомендаций
# Функция хэша нормальная?
# Как локализировать?
# todo:
#     Сохранение нейронки--
#     Ребочие теги --
#     Сервер
#         Оптимизация хранения данных --
#         Многопоточность --
#         Как синхронизировать оценки? --
#     Цели --

#Так распределить свой день, что бы достичь цели
#Обучение за счет психологии
#анимация или видео

# 26 билд
# 24 функции 22:00
# todo github


# БЖД
# Экономика
# Дневник:
# Актуальность
# Положения
# Методы
# Алгоритмы
# Новизна
# от 0 до приложения (спецчасть)
# 02.06 5:30
#
# 26.05 23:00
