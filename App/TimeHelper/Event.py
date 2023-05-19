class event:


    def __init__(self, date, time, description):
        '''
        Класс, предстовлябщий собой событие
        Параметры:
        Date - дата события
        Time - время события
        duration - продолижтельность в минутах
        Description - Описание (как правло мловарь с набором тегов, иначе бедет воспрянт как один парметр other)
        '''
        events = []
        self.date = date
        self.time = time
        if type(description) is dict:
            self.descripton = description
            if not("duration" in self.descripton):
                self.descripton["duration"] = 45
        else:
            self.descripton = {
                "duration": 45,
                "other": description
            }

        # добавление количество минут от начала дня дня
        mins = time.split(":")
        mins = int(mins[0]) * 60 + int(mins[1])
        self.descripton["time"] = mins
        # if self.descripton["duration"] > 45:
        #     d = description
        #     d["duration"] = d["duration"] - 45
        #     t = dt.time.fromisoformat(time)
        #     t = (dt.datetime.combine(dt.date(1, 1, 1), t) + dt.timedelta(minutes=45)).time().strftime('%H:%M')
        #     print(t)
        #     self.__init__(date, t, d)




    @property
    def name(self):
        return self.descripton["name"]

    @property
    def description(self):
        return self.descripton

    @property
    def duration(self):
        return self.descripton["duration"]

    #нужно переписать, не обновляет теги
    def edit(self,date=None, time=None, dur=0, description = None):
        if date !=None:
            self.date = date
        if time !=None:
            self.time = time
        if dur != 0:
            self.dur = dur
        if description != None:
            if description is dict:
                self.descripton = description

