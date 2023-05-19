from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton
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

DAYS = 7
TAGH = 25

class MainScreen(Screen):


    def __init__(self, name):
        super(MainScreen, self).__init__(name = name)
        d = days()
        for i in range(DAYS):
            s = f"day{i}"
            self.ids[s].text = d[i]

    def btn_touch_up(self,id):
        print(f"Touch Up {id}")
        print(self.ids)
        D = self.manager.get_screen("Day")

        D.ids['L1'].text = self.ids[id].text
        events = TestApp.L.get_day(self.ids[id].text.split()[1])
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

    def form_btn_touch_up(self, fn):
        F = self.manager.get_screen("Form")
        file = open(fn, 'r')
        for i,line in enumerate(file):
            line = line.split(';')
            if line[0] == "S":
                F.ids["questionsbox"].add_widget(SimpleQuestion(text = line[1], group = f"{line[1]}"))
            else:
                F.ids["questionsbox"].add_widget(RateQuestion(text = line[1], LL = line[2], RL = line[3]))
            print(F.ids["questionsbox"].children[0].text)
            F.ids["questionsbox"].height += 120

        self.manager.current = "Form"

    def BGNight(self):
        pass



class DayButton(MDRectangleFlatButton):
        pass

class EVENT(BoxLayout):
    pass

class Form(Screen):

    def close_btn_touch_up(self):
        self.manager.current = "MainScreen"
        box = self.ids['questionsbox']
        childs = [i for i in box.children]
        for i in childs:
            box.remove_widget(i)
        box.height = 0

class SimpleQuestion(BoxLayout):
    text = StringProperty()
    group = StringProperty()

class RateQuestion(BoxLayout):
    text = StringProperty()
    LL = StringProperty("0")
    RL = StringProperty("10")
class Day(Screen):

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
        date = TestApp.L.recomendation(event)
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
        TestApp.L.addevent(name = self.ids['name'].text,
                           time = self.ids['time'].text,
                           date = self.ids['date'].text,
                           descript= tags)
        self.close_btn_touch_up()

class GCheckItem(MDBoxLayout):
    text = StringProperty()
    group = StringProperty()

class CheckItem(MDBoxLayout):
    text = StringProperty()


class TestApp(MDApp):

    L = Logic()

    def build(self):
        self.MS = MainScreen(name="MainScreen")
        self.DS = Day(name="Day")
        self.ES = NEWEVENT(name="NEWEVENT")
        self.F = Form(name = "Form")
        self.sm = ScreenManager()

        self.sm.add_widget(self.MS)
        self.sm.add_widget(self.DS)
        self.sm.add_widget(self.ES)
        self.sm.add_widget(self.F)

        return self.sm


#todo Косяк с файлом сейва, поправить при билде
TestApp().run()