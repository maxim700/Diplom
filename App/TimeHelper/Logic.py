from Calendar import *
from Brain import *
from ExpBank import *
import datetime as dt
import TAGS

class Logic():

    def __init__(self):
        self.C = calendar()
        self.Bank = ExpBank()
        self.optimazer = Adam(learning_rate=0.01)
        self.key = "TEST"#todo hash
        self.Brain = Agent(self.C, self.optimazer, self.Bank, self.key)
        self.Brain._build_compile_model()

        try:
            self.C.load()
        except:
            self.C.save()

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

    def recomendation(self, event):
        tdr = dates.today_range()
        print(tdr)
        state = self.C.format(self.C.get_period(tdr[0], tdr[1]))
        print(state)
        state = state + event
        action = self.Brain.act(state)
        today = dt.datetime.today()
        date = today + dt.timedelta(action+1)
        print(date)
        return date

    def addevent(self, name, date, time, descript):
        print(name, date, time, descript)


# Что хоти видеть в профиле? - skills mbti name
# Нужны ли настройки? Какие? цвета
# На что завизать опросы - кнопочка оценка рекомендаций
# Функция хэша нормальная?
# Как локализировать?
# todo:
#     Сохранение нейронки
#     Ребочие теги
#     Сервер
#         Оптимизация хранения данных
#         Многопоточность
#         Как синхронизировать оценки?
#     Цели

#Так распределить свой день, что бы достичь цели
#Обучение за счет психологии
#анимация или видео

# 26 билд
# 24 функции 22:00
# todo github
