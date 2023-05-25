from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton, MDRaisedButton, MDRectangleFlatIconButton
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty
from kivymd.uix.pickers.timepicker.timepicker import MDTimePicker
from  kivymd.uix.pickers.datepicker.datepicker import MDDatePicker

from Logic import *
from dates import days
import datetime as dt
import TAGS
from threading import Thread

DAYS = 7
TAGH = 25

class MainScreen(Screen):

    def __init__(self, name, Logic, Settings):
        super(MainScreen, self).__init__(name = name)
        self.Logic = Logic
        self.Settings = Settings
        d = days()
        for i in range(DAYS):
            s = f"day{i}"
            self.ids[s].text = d[i]

    def day_btn_touch_up(self,id):
        print(f"Touch Up {id}")
        print(self.ids)
        D = self.manager.get_screen("Day")

        D.ids['L1'].text = self.ids[id].text
        events = self.Logic.get_day(self.ids[id].text.split()[1])
        if not(events is None):
            print(len(events))
            for event in events:
                e = EVENT()
                e.ids["L1"].text = f"{event[0]} {event[1]}:"
                for tag in event[2]:
                    e.ids["tagbox"].add_widget(TAG(text = tag))

                e.ids['tagbox'].add_widget(Widget())
                D.ids['box'].add_widget(e)
            print('height')
            print(D.ids['eslayout'].height)
            D.ids['eslayout'].height = len(events)*(TAGH+5)*4
            print(D.ids['eslayout'].height)

        self.manager.current = "Day"

    def add_btn_touch_up(self):

        E = self.manager.get_screen("NEWEVENT")
        for tag in TAGS.TAGS:
            E.ids["tagbox"].add_widget(CheckItem(text = tag, id = tag))

        self.manager.current = "NEWEVENT"

    def rate_btn_touch_up(self):
        RS = self.manager.get_screen("RateScreen")
        NR = self.Logic.get_needrate()
        for i in NR.keys():
            RS.ids["ratebox"].add_widget(RateButton(text = i))
            RS.ids['ratebox'].height += 60
        self.manager.current = "RateScreen"


    def profile_btn_touch_up(self):
        P = self.manager.get_screen("Profile")
        skills = self.Logic.get_skills()
        for skill in skills.keys():
            P.ids['skillsbox'].add_widget(SkillButton(text = str(skills[skill]), icon = self.Settings["icons"][skill]))
            P.ids['skillsbox'].height +=60
        self.manager.current = "Profile"

    def on_save_date(self, instance, value, date_range):
        print(value)

    def calendare_btn_toch_up(self):
        today = dt.date.today()
        date_dialog = MDDatePicker(year=today.year, month=today.month, day=today.day)
        date_dialog.bind(on_save=self.on_save_date)
        date_dialog.open()


    def BGNight(self):
        pass

class SkillButton(MDRectangleFlatIconButton):
    text = StringProperty()
    icon = StringProperty()

class DayButton(MDRaisedButton):
        pass

class EVENT(BoxLayout):
    pass

class Form(Screen):
    ButtonText = StringProperty("Завершить")
    ResultPath = StringProperty("Завершить")

    def __init__(self,name,Logic,Settings):
        super(Form, self).__init__(name= name)
        self.Logic = Logic
        self.Settings = Settings

    def close_btn_touch_up(self,ResultPath):
        rate = []
        self.manager.current = "MainScreen"
        box = self.ids['questionsbox']
        childs = [i for i in box.children]
        for i in childs:
            if i is SimpleQuestion:
                if i.ids['check'].active:
                    rate.append(1)
                else:
                    rate.append(0)
            else:
                 rate.append(i.ids['rate'].value)
            box.remove_widget(i)
        box.height = 0
        self.Logic.set_LastForm(rate)
        self.Logic.use_LastForm(ResultPath)


class SimpleQuestion(BoxLayout):
    text = StringProperty()
    group = StringProperty()

class RateQuestion(BoxLayout):
    text = StringProperty()
    LL = StringProperty("0")
    RL = StringProperty("10")

    def int_on_touch_up(self):
        self.ids["rate"].value = int(self.ids["rate"].value)

class Day(Screen):

    def __init__(self,name,Logic,Settings):
        super(Day, self).__init__(name= name)
        self.Logic = Logic
        self.Settings = Settings

    def rename(self):
        print(self.ids)

    def close_btn_touch_up(self):
        self.manager.current = "MainScreen"
        box = self.ids['box']
        childs = [i for i in box.children]
        for i in childs:
            box.remove_widget(i)



class TAG(Label):
    pass

class NEWEVENT(Screen):

    def __init__(self,name,Logic,Settings):
        super(NEWEVENT, self).__init__(name= name)
        self.Logic = Logic
        self.Settings = Settings

    def set_time(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time, on_save = self.on_save_time)
        time_dialog.open()


    def get_time(self, instance, time):
        '''
        The method returns the set time.

        :type instance: <kivymd.uix.picker.MDTimePicker object>
        :type time: <class 'datetime.time'>
        '''

        return time

    def on_save_time(self,instance, time):
        self._time = time
        self.ids["time"].text = time.strftime('%H:%M')

    def on_save_date(self, instance, value, date_range):
        self.ids["date"].text = value.strftime('%d.%m.%Y')

    def set_date(self):
        today = dt.date.today()
        date_dialog = MDDatePicker(year=today.year, month=today.month, day=today.day)
        date_dialog.bind(on_save=self.on_save_date)
        date_dialog.open()


    def rec_btn_touch_up(self):
        event = []
        childrens = [self.ids['tagbox'].children[i] for i in range(len(TAGS.TAGS))]
        for child in childrens:
             if child.ids['check'].active:
                 event.append(child.id)
        print(event)
        date = self.Logic.recomendation(event)
        self.ids["date"].text = date.strftime('%d.%m.%Y')

    def close_btn_touch_up(self):
        self.manager.current = "MainScreen"
        box = self.ids['tagbox']
        childs = [i for i in box.children]
        for i in childs:
            box.remove_widget(i)
        self.ids['name'].text = ""
        self.ids['time'].text = "Time"
        self.ids['date'].text = "Date"

    def ok_btn_touch_up(self):
        tags = [self.ids['tagbox'].children[i].id for i in range(len(TAGS.TAGS)) if self.ids['tagbox'].children[i].ids['check'].active]
        descr = {"name":self.ids['name'].text}
        for i in tags:
            descr[i] = True
        self.Logic.addevent(time = self.ids['time'].text,
                           date = self.ids['date'].text,
                           descript= descr)
        self.close_btn_touch_up()

class GCheckItem(MDBoxLayout):
    text = StringProperty()
    group = StringProperty()

class CheckItem(MDBoxLayout):
    text = StringProperty()

class Profile(Screen):
    ProfileHead = StringProperty("Ваш профиль")
    ButtonText =  StringProperty("Закрыть")

    def __init__(self, name, Logic, Settings):
        super(Profile, self).__init__(name=name)
        self.Logic = Logic
        self.Settings = Settings

    def close_btn_touch_up(self):
        self.manager.current = "MainScreen"
        box = self.ids['skillsbox']
        childs = [i for i in box.children]
        for i in childs:
            box.remove_widget(i)

class RateScreen(Screen):
    Header = StringProperty("События ожидающие оценки")
    ButtonText = StringProperty("Закрыть")

    def __init__(self,name,Logic,Settings, FC):
        super(RateScreen, self).__init__(name= name)
        self.Logic = Logic
        self.Settings = Settings
        self.FC = FC

    def close_btn_touch_up(self):
        self.manager.current = "MainScreen"
        box = self.ids['ratebox']
        childs = [i for i in box.children]
        for i in childs:
            box.remove_widget(i)
        box.height = 0

class RateButton(MDRaisedButton):
    text = StringProperty("Закрыть")


class Reg(Screen):
    #Все тексты буду подгружаться из файла локализации
    LabelText = StringProperty("Добро пожаловаь")
    ButtonText = StringProperty("Зарегестрироваться")

    def __init__(self,name,Logic,Settings, FC):
        super(Reg, self).__init__(name= name)
        self.Logic = Logic
        self.Settings = Settings
        self.FC = FC

    def reg_btn_touch_up(self):
        self.FC("RegForm.json",result = "Skills")



class TestApp(MDApp):

    L = Logic()

    def __init__(self):
        super(TestApp, self).__init__()
        t1 = Thread(target=self.L.update_data, daemon=True)
        t1.start()
        self.load_setting()

    def load_setting(self):
        try:
            with open("Settings.json", "r") as file:
                self.Settings = json.load(file)
            file.close()
            return True
        except Exception as e:
            print(e)
            return False

    def form_constructor(self,fn,result):
        F = self.sm.get_screen("Form")
        F.ResultPath = result
        try:
            with open(fn, "r") as file:
                data = json.load(file)["form"]
            for i, line in enumerate(data):
                if line[0] == "S":
                    F.ids["questionsbox"].add_widget(SimpleQuestion(text=line[1], group=f"{line[1]}"))
                else:
                    F.ids["questionsbox"].add_widget(RateQuestion(text=line[1], LL=line[2], RL=line[3]))
                print(F.ids["questionsbox"].children[0].text)
                F.ids["questionsbox"].height += 120


            self.sm.current = "Form"
        except Exception as e:
            print(e)
            self.sm.current = "MainScreen"



    def build(self):
        self.MS = MainScreen(name="MainScreen", Logic=self.L,Settings=self.Settings)
        self.DS = Day(name="Day", Logic=self.L,Settings=self.Settings)
        self.ES = NEWEVENT(name="NEWEVENT", Logic=self.L,Settings=self.Settings)
        self.F = Form(name = "Form", Logic=self.L,Settings=self.Settings)
        self.P = Profile(name="Profile", Logic=self.L,Settings=self.Settings)
        self.R = Reg(name="Reg", Logic=self.L,Settings=self.Settings, FC = self.form_constructor)
        self.RS = RateScreen(name="RateScreen", Logic=self.L, Settings=self.Settings, FC=self.form_constructor)

        self.sm = ScreenManager()

        self.sm.add_widget(self.MS)
        self.sm.add_widget(self.DS)
        self.sm.add_widget(self.ES)
        self.sm.add_widget(self.F)
        self.sm.add_widget(self.P)
        self.sm.add_widget(self.R)
        self.sm.add_widget(self.RS)

        if not(self.L.loadprofile()):
            self.sm.current = "Reg"

        return self.sm


#todo Косяк с файлом сейва, поправить при билде
TestApp().run()