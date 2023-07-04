from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton, MDRaisedButton, MDRectangleFlatIconButton, MDFillRoundFlatIconButton
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ListProperty
from kivymd.uix.pickers.timepicker.timepicker import MDTimePicker
from kivymd.uix.pickers.datepicker.datepicker import MDDatePicker
import matplotlib.pyplot as plt
import os


from Logic import *
from dates import days
import datetime as dt
import TAGS
from threading import Thread

class MainScreen(Screen):
    AppName = StringProperty()

    def __init__(self, name, APP):
        super(MainScreen, self).__init__(name = name)
        self.APP = APP
        self.Logic = APP.Logic
        self.Settings = APP.Settings
        self.FC = APP.form_constructor

    def show(self):
        self.AppName = self.APP.Lang["MainScreen"]["Header"]
        d = days(self.APP.Lang["MainScreen"]["Days"])
        for i in range(7):
            s = f"day{i}"
            self.ids[s].text = d[i]
        self.manager.current = "MainScreen"

    def fill_days(self,D,events):
        for event in events:
            e = EVENT()
            cols = e.ids["tagbox"].cols
            e.ids["L1"].text = f"  {event[0]} {event[1]}:"
            for i,tag in enumerate(event[2]):
                e.ids["tagbox"].add_widget(TAG(TagText=self.APP.Lang["NewEvent"]["TagName"][tag]))
                if i%cols == 0:
                    e.ids['tagbox'].height += 60
                    D.ids['eslayout'].height += 85

            e.ids['tagbox'].add_widget(Widget())
            D.ids['box'].add_widget(e)



    def day_btn_touch_up(self,id):
        print(f"Touch Up {id}")
        print(self.ids)
        D = self.manager.get_screen("Day")

        D.ids['L1'].text = f"   {self.ids[id].text}"
        events = self.Logic.get_day(self.ids[id].text.split()[1])
        if not(events is None):
            print(len(events))
            self.fill_days(D,events)
        else:
            D.add_widget(FloatLabel(LabelText=self.APP.Lang["Common"]["Void"]))
        D.show()

    def add_btn_touch_up(self):
        E = self.manager.get_screen("NEWEVENT")
        E.show()

    def rate_btn_touch_up(self):
        RS = self.manager.get_screen("RateScreen")
        RS.show()


    def profile_btn_touch_up(self):
        P = self.manager.get_screen("Profile")
        P.show()

    def on_save_date(self, instance, value, date_range):
        date = value.strftime('%d.%m.%Y')
        D = self.manager.get_screen("Day")
        D.ids['L1'].text = f"   {date}"
        events = self.Logic.get_day(date)
        if not (events is None):
            print(len(events))
            self.fill_days(D,events)
        else:
            D.add_widget(FloatLabel(LabelText=self.APP.Lang["Common"]["Void"]))
        self.manager.current = "Day"

    def calendare_btn_toch_up(self):
        today = dt.date.today()
        date_dialog = DateDialog(year=today.year, month=today.month, day=today.day)
        date_dialog.bind(on_save=self.on_save_date)
        date_dialog.open()

    def Task_btn_toch_up(self):
        T = self.manager.get_screen("TaskScreen")
        T.show()

    def close_btn_touch_up(self):
        pass

class DayButton(MDRaisedButton):
    pass

class EVENT(BoxLayout):
    pass

class Form(Screen):
    ButtonText = StringProperty("Завершить")
    ResultPath = StringProperty()

    def __init__(self,name,APP):
        super(Form, self).__init__(name= name)
        self.APP = APP
        self.Logic = APP.Logic
        self.Settings = APP.Settings
        self.otherdata = None
        self.BackScreen = "MainScreen"

    def close_btn_touch_up(self,ResultPath):
        rate = []
        box = self.ids['questionsbox']
        childs = [i for i in box.children]
        for i in childs:
            if i is SimpleQuestion:
                if i.ids["check"].active:
                    rate.append(1)
                else:
                    rate.append(0)
            else:
                 rate.append(i.ids['rate'].value)
            box.remove_widget(i)
        box.height = 0
        self.Logic.set_LastForm(rate)
        self.Logic.use_LastForm(ResultPath, self.otherdata)
        self.otherdata = None
        SC = self.manager.get_screen(self.BackScreen)
        self.BackScreen = "MainScreen"
        SC.close_btn_touch_up()
        SC.show()





class SimpleQuestion(BoxLayout):
    text = StringProperty()
    group = StringProperty()
    Yes = StringProperty()
    No = StringProperty()

class RateQuestion(BoxLayout):
    text = StringProperty()
    LL = StringProperty("0")
    RL = StringProperty("10")

    def int_on_touch_up(self):
        self.ids["rate"].value = int(self.ids["rate"].value)

class Day(Screen):
    CloseButton = StringProperty()

    def __init__(self,name, APP):
        super(Day, self).__init__(name= name)
        self.APP = APP
        self.Logic = APP.Logic
        self.Settings = APP.Settings

    def rename(self):
        print(self.ids)

    def show(self):
        self.CloseButton = self.APP.Lang["Common"]["Close"]
        self.manager.current = "Day"

    def close_btn_touch_up(self):
        box = self.ids['box']
        childs = [i for i in box.children]
        for i in childs:
            box.remove_widget(i)
        if "FL" in self.ids.keys():
            self.remove_widget(self.ids["FL"])
        MS = self.manager.get_screen("MainScreen")
        MS.show()
        self.ids['eslayout'].height = 20




class TAG(Label):
    TagText = StringProperty()

class NEWEVENT(Screen):
    Name = StringProperty()
    Tags = StringProperty()
    TimeS = StringProperty()
    TimeF = StringProperty()
    Date = StringProperty()
    OkButton = StringProperty()
    CloseButton = StringProperty()


    def __init__(self,name,APP):
        super(NEWEVENT, self).__init__(name= name)
        self.APP = APP
        self.Logic = APP.Logic
        self.Settings = APP.Settings

    def show(self):
        self.Name = self.APP.Lang["NewEvent"]["Name"]
        self.Tags = self.APP.Lang["NewEvent"]["Tags"]
        self.TimeS = self.APP.Lang["NewEvent"]["TimeS"]
        self.TimeF = self.APP.Lang["NewEvent"]["TimeF"]
        self.Date = self.APP.Lang["NewEvent"]["Date"]
        self.CloseButton = self.APP.Lang["Common"]["Close"]
        self.OkButton = self.APP.Lang["Common"]["Ok"]
        for tag in TAGS.TAGS:
            self.ids["tagbox"].add_widget(CheckItem(text = self.APP.Lang["NewEvent"]["TagName"][tag], id = tag))
        self.manager.current = "NEWEVENT"

    def set_time(self, start = True):
        time_dialog = TimeDialog()
        if start:
            time_dialog.bind(time=self.get_time, on_save = self.on_save_time_start)
        else:
            time_dialog.bind(time=self.get_time, on_save=self.on_save_time_finish)
        time_dialog.open()


    def get_time(self, instance, time):
        return time

    def on_save_time_start(self,instance, time):
        self.ids["times"].text = time.strftime('%H:%M')

    def on_save_time_finish(self,instance, time):
        self.ids["timef"].text = time.strftime('%H:%M')

    def on_save_date(self, instance, value, date_range):
        self.ids["date"].text = value.strftime('%d.%m.%Y')

    def set_date(self):
        today = dt.date.today()
        date_dialog = DateDialog(year=today.year, month=today.month, day=today.day)
        date_dialog.bind(on_save=self.on_save_date)
        date_dialog.open()


    def rec_btn_touch_up(self):
        event = []
        childrens = [self.ids['tagbox'].children[i] for i in range(len(TAGS.TAGS))]
        for child in childrens:
             if child.ids["check"].active:
                 event.append(child.id)
        print("#######EVENT###########")
        print(event)
        date = self.Logic.recomendation(event)
        self.ids["date"].text = date.strftime('%d.%m.%Y')
        self.add_widget(ModalCase(name=self.APP.Lang["Common"]["Rec"], text=date.strftime('%d.%m.%Y'), id="info", sc=self))

    def close_btn_touch_up(self):
        box = self.ids['tagbox']
        childs = [i for i in box.children]
        for i in childs:
            box.remove_widget(i)
        MS = self.manager.get_screen("MainScreen")
        MS.show()

    def ok_btn_touch_up(self):
        tags = [self.ids['tagbox'].children[i].id for i in range(len(TAGS.TAGS)) if self.ids['tagbox'].children[i].ids['check'].active]
        descr = {"name":self.ids['name'].text}
        dur = dt.datetime.strptime(self.ids['timef'].text, "%H:%M") - dt.datetime.strptime(self.ids['times'].text, "%H:%M")
        descr["duration"] =  dur.seconds//60

        for i in tags:
            descr[i] = True
        self.Logic.addevent(time = self.ids['times'].text,
                           date = self.ids['date'].text,
                           descript= descr)
        self.close_btn_touch_up()

class GCheckItem(MDBoxLayout):
    text = StringProperty()
    group = StringProperty()
    checked = BooleanProperty(False)

class DateDialog(MDDatePicker):
    pass

class TimeDialog(MDTimePicker):
    pass

class CheckItem(MDBoxLayout):
    text = StringProperty()
    checked = BooleanProperty(False)

class Profile(Screen):
    ProfileHead = StringProperty()
    ButtonText =  StringProperty()
    LangButton = StringProperty()
    Theme = StringProperty()


    def __init__(self, name, APP):
        super(Profile, self).__init__(name=name)
        self.APP = APP
        self.Logic = APP.Logic
        self.Settings = APP.Settings

    def show(self):
        self.ProfileHead = self.APP.Lang["Profile"]["Header"]
        self.LangButton = self.Settings["Lang"]
        self.ButtonText = self.APP.Lang["Common"]["Close"]
        if self.Settings["Theme"]=="Dark":
            self.Theme = "weather-night"
        else:
            self.Theme = "white-balance-sunny"
        skills = self.Logic.get_skills()
        for skill in skills.keys():
            self.ids['skillsbox'].add_widget(SkillButton(text=str(skills[skill]), icon=self.Settings["icons"][skill], skill = skill, sc = self))
            self.ids['skillsbox'].height += 30
        self.manager.current = "Profile"

    def settings_btn_touch_up(self):
        SS = self.manager.get_screen("SettingScreen")
        SS.show()

    def close_btn_touch_up(self):
        box = self.ids['skillsbox']
        childs = [i for i in box.children]
        for i in childs:
            box.remove_widget(i)
        box.height = 0
        MS = self.manager.get_screen("MainScreen")
        MS.show()


class SkillButton(MDFillRoundFlatIconButton):
    text = StringProperty()
    icon = StringProperty()

    def __init__(self, text, icon, skill, sc):
        super(SkillButton, self).__init__()
        self.text = text
        self.icon = icon
        self.skill = skill
        self.sc = sc

    def showinfo(self):
        name = self.sc.APP.Lang["Profile"][self.skill]
        self.sc.add_widget(ModalCase(name=name[0], text=name[1], id="info", sc=self.sc))

class ModalCase(BoxLayout):
    name = StringProperty()
    text = StringProperty()
    CloseButtonText = StringProperty()

    def __init__(self, name, text, id, sc):
        super(ModalCase, self).__init__()
        self.name = name
        self.text = text
        self.sc = sc
        self.CloseButtonText = sc.APP.Lang["Common"]["Close"]

    def close_btn_touch_up(self):
        self.sc.remove_widget(self)


class SettingScreen(Screen):
    Header = StringProperty()
    CloseButtonText = StringProperty()
    Theme = StringProperty()
    LangName = StringProperty()

    def __init__(self,name, APP):
        super(SettingScreen, self).__init__(name= name)
        self.APP = APP
        self.Logic = APP.Logic
        self.Settings = APP.Settings


    def show(self):
        self.LangName = self.Settings["Lang"]
        self.Theme = self.APP.Lang["Theme"][self.Settings["Theme"]]
        self.Header = self.APP.Lang["Settings"]["Header"]
        self.CloseButtonText = self.APP.Lang["Common"]["Save"]
        self.manager.current = "SettingScreen"

    def change_lang_btn_touch_up(self):
        if self.LangName == "EN":
            self.LangName = "RU"
            self.Settings["Lang"] = "RU"
        else:
            self.LangName = "EN"
            self.Settings["Lang"] = "EN"

        self.APP.set_lang()


    def change_theme_btn_touch_up(self):
        if self.Settings["Theme"] == "Dark":
            self.Theme = self.APP.Lang["Theme"]["Light"]
            self.Settings["Theme"] = "Light"
        else:
            self.Theme = self.APP.Lang["Theme"]["Dark"]
            self.Settings["Theme"] = "Dark"
        print(self.Settings["Theme"])
        self.APP.set_colors()


    def close_btn_touch_up(self):
        self.APP.save_settings()
        PS = self.manager.get_screen("Profile")
        PS.close_btn_touch_up()
        PS.show()



class RateScreen(Screen):
    Header = StringProperty("События ожидающие оценки")
    ButtonText = StringProperty("Закрыть")

    def __init__(self,name, APP):
        super(RateScreen, self).__init__(name= name)
        self.APP = APP
        self.Logic = APP.Logic
        self.Settings = APP.Settings
        self.FC = APP.form_constructor

    def show(self):
        NR = self.Logic.get_needrate()
        if len(NR.keys())>0:
            for i in NR.keys():
                self.ids["ratebox"].add_widget(RateButton(text=NR[i], eventid=i, FC=self.FC, Lang=self.APP.Lang))
                self.ids['ratebox'].height += 60
        else:
            self.add_widget(FloatLabel(LabelText = self.APP.Lang["Common"]["Void"]))
        self.manager.current = "RateScreen"

    def close_btn_touch_up(self):
        box = self.ids['ratebox']
        childs = [i for i in box.children]
        for i in childs:
            box.remove_widget(i)
        box.height = 0
        if "FL" in self.ids.keys():
            self.remove_widget(self.ids["FL"])
        MS = self.manager.get_screen("MainScreen")
        MS.show()


class RateButton(MDRaisedButton):
    text = StringProperty()
    eventid = StringProperty()

    def __init__(self,text, eventid, Lang, FC):
        super(RateButton, self).__init__()
        self.FC = FC
        self.text = text
        self.eventid = eventid
        self.Lang = Lang

    def rate_btn_touch_up(self, eventid):
        self.FC(fn = "RateForm", result = "Rate", backscreen = "RateScreen", otherdata = self.eventid)


class Reg(Screen):
    #Все тексты буду подгружаться из файла локализации
    LabelText = StringProperty()
    ButtonText = StringProperty()

    def __init__(self,name,APP):
        super(Reg, self).__init__(name= name)
        self.APP = APP
        self.Logic = APP.Logic
        self.Settings = APP.Settings
        self.FC = APP.form_constructor

    def show(self):
        self.LabelText = self.APP.Lang["Reg"]["Header"]
        self.ButtonText = self.APP.Lang["Reg"]["Start"]
        self.manager.current = "Reg"

    def reg_btn_touch_up(self):
        self.FC("RegForm",result = "Skills")

class StatScreen(Screen):
    Header = StringProperty()
    CloseButton = StringProperty()

    def __init__(self,name,APP):
        super(StatScreen, self).__init__(name= name)
        self.APP = APP
        self.Logic = APP.Logic
        self.Settings = APP.Settings

    def show(self):
        self.Header = self.APP.Lang["StatScreen"]["Header"]
        self.CloseButton = self.APP.Lang["Common"]["Close"]

        stat = self.Logic.get_task_stat()
        print(stat)
        if sum(stat) != 0:
            plt.pie(stat, labels= self.APP.Lang["TaskScreen"]["Stat"])
            plt.savefig("stat.png")
            # MatplotFigure (Kivy widget)
            #self.ids["graph"].add_widget(FigureCanvasKivyAgg(plt.gcf()))
            self.ids["graph"].add_widget(Image(source='stat.png'))
            os.remove('stat.png')
        else:
            self.add_widget(FloatLabel(LabelText=self.APP.Lang["Common"]["Void"]))
        self.manager.current = "StatScreen"

    def close_btn_touch_up(self):
        box = self.ids['graph']
        childs = [i for i in box.children]
        for i in childs:
            box.remove_widget(i)
        TS = self.manager.get_screen("TaskScreen")
        TS.close_btn_touch_up()
        TS.show()

class TaskScreen(Screen):
    TaskHeader = StringProperty()
    CloseButton = StringProperty()

    def __init__(self,name,APP):
        super(TaskScreen, self).__init__(name= name)
        self.APP = APP
        self.Logic = APP.Logic
        self.Settings = APP.Settings

    def newtask_btn_touch_up(self):
        NTS = self.manager.get_screen("NewTaskScreen")
        NTS.show()

    def stat_btn_touch_up(self):
        ST = self.manager.get_screen("StatScreen")
        ST.show()


    def show(self):
        self.TaskHeader = self.APP.Lang["TaskScreen"]["Header"]
        self.CloseButton = self.APP.Lang["Common"]["Close"]
        tasks = self.Logic.get_tasks()
        if len(tasks.keys())>0:
            for task in tasks.keys():
                self.ids['taskbox'].add_widget(Task(task=task, Logic=self.Logic, sm=self.manager, Lang=self.APP.Lang))
                self.ids['taskbox'].height += 80
        else:
            self.add_widget(FloatLabel(LabelText = self.APP.Lang["Common"]["Void"]))
        self.manager.current = "TaskScreen"

    def close_btn_touch_up(self):
        box = self.ids['taskbox']
        childs = [i for i in box.children]
        for i in childs:
            box.remove_widget(i)
        box.height = 0
        print(self.children)
        if "FL" in self.ids.keys():
            self.remove_widget(self.ids["FL"])
        MS = self.manager.get_screen("MainScreen")
        MS.show()

class Task(BoxLayout):
    name = StringProperty()
    value = NumericProperty()
    max = NumericProperty()
    SubTaskButton = StringProperty()

    def __init__(self,task, Logic, sm, Lang):
        super(Task, self).__init__()
        self.Logic = Logic
        self.sm = sm
        self.Lang = Lang
        self.task = task
        self.name = task.split()[0]
        self.max, self.value = self.Logic.get_task_progress(task)
        self.SubTaskButton = self.Lang["Common"]["Open"]
        print(f"TASK: {self.value} {self.max}")
        print(f"TASK: {self.ids['bar'].value} {self.ids['bar'].max}")

    def subtask_btn_toch_up(self):
        STS = self.sm.get_screen("SubTaskScreen")
        STS.show(self.name, self.task)


class NewTaskScreen(Screen):
    Name = StringProperty()
    AddButton = StringProperty()


    def __init__(self,name,APP):
        super(NewTaskScreen, self).__init__(name= name)
        self.APP = APP
        self.Logic = APP.Logic
        self.Settings = APP.Settings

    def show(self):
        self.Name = self.APP.Lang["NewTaskScreen"]["Name"]
        self.AddButton = self.APP.Lang["NewTaskScreen"]["Add"]
        self.manager.current = "NewTaskScreen"

    def newsubtask_btn_touch_up(self):
        self.ids["newtaskbox"].height += 80
        self.ids["newtaskbox"].add_widget(NewSubTask(Name = self.APP.Lang["Common"]["Name"]))

    def close_btn_touch_up(self):
        name = self.ids['name'].text
        self.ids['name'].text = ""
        subtasks = {}
        box = self.ids['newtaskbox']
        childs = [i for i in box.children]
        for i in childs:
            subtasks[i.ids["name"].text] = False
            box.remove_widget(i)
        box.height = 0
        self.Logic.addTask(name, subtasks)
        TS = self.manager.get_screen("TaskScreen")
        TS.close_btn_touch_up()
        TS.show()

class NewSubTask(BoxLayout):
    Name = StringProperty()

class SubTaskScreen(Screen):
    text = StringProperty()
    task = StringProperty()
    CloseButton = StringProperty()

    def __init__(self,name, APP):
        super(SubTaskScreen, self).__init__(name= name)
        self.APP = APP
        self.Logic = APP.Logic
        self.Settings = APP.Settings

    def show(self, name, task):
        self.CloseButton = self.APP.Lang["Common"]["Close"]
        self.text = name
        self.task = task
        task = self.Logic.get_task(task)
        for subtask in task.keys():
            print(task[subtask])
            self.ids['subtaskbox'].add_widget(SubTask(text=subtask, checked=task[subtask]))
            self.ids['subtaskbox'].height += 60
        self.manager.current = "SubTaskScreen"

    def close_btn_touch_up(self):
        subtasks = {}
        box = self.ids['subtaskbox']
        childs = [i for i in box.children]
        for i in reversed(childs):
            subtasks[i.text] = i.ids["check"].ids["check"].active
            box.remove_widget(i)
        box.height = 0
        print(subtasks)
        self.Logic.set_task_progress(self.task, subtasks)
        TS = self.manager.get_screen("TaskScreen")
        TS.close_btn_touch_up()
        MS = self.manager.get_screen("MainScreen")
        MS.Task_btn_toch_up()


class SubTask(BoxLayout):
    text = StringProperty()
    checked = BooleanProperty()

class FloatLabel(Label):
    LabelText = StringProperty()

class TestApp(MDApp):

    Logic = Logic()
    BGC = StringProperty()
    AC = StringProperty()
    PBC = StringProperty()
    SBC = StringProperty()
    TC = StringProperty()
    font_size = NumericProperty(16)

    def __init__(self):
        super(TestApp, self).__init__()
        t1 = Thread(target=self.Logic.update_data, daemon=True)
        t1.start()
        self.load_setting()

    def load_setting(self):
        try:
            with open("Settings.json", "r") as file:
                self.Settings = json.load(file)
            file.close()
            self.set_lang()
            self.set_colors()
            return True
        except Exception as e:
            print(e)
            return False

    def save_settings(self):
        with open("Settings.json", "w") as file:
            json.dump(self.Settings,file)
        file.close()

    def set_lang(self):
        try:
            print(self.Settings["Lang"])
            with open(self.Settings["Lang"] + ".json", "r") as file:
                self.Lang = json.load(file)
            file.close()
        except:
            with open("EN.json", "r") as file:
                self.Lang = json.load(file)
            file.close()

    def set_colors(self):
        if self.Settings["Theme"] == "Dark":
            self.Colors = self.Settings["DColors"]
        else:
            self.Colors = self.Settings["LColors"]
        self.BGC = self.Colors["BGC"]
        self.AC = self.Colors["AC"]
        self.PBC = self.Colors["PBC"]
        self.SBC = self.Colors["SBC"]
        self.TC = self.Colors["TC"]
        self.OC1 = self.Colors["OC1"]

    def form_constructor(self,fn,result, backscreen = "MainScreen", otherdata = None):
        F = self.sm.get_screen("Form")
        F.ResultPath = result
        F.otherdata = otherdata
        F.BackScreen = backscreen
        try:
            with open(fn+f"{self.Settings['Lang']}.json", "r") as file:
                data = json.load(file)["form"]
            for i, line in enumerate(data):
                if line[0] == "S":
                    F.ids["questionsbox"].add_widget(SimpleQuestion(text=line[1], group=f"{line[1]}", Yes = self.Lang["Common"]["Yes"], No = self.Lang["Common"]["No"]))
                else:
                    F.ids["questionsbox"].add_widget(RateQuestion(text=f"  {line[1]}", LL=line[2], RL=line[3]))
                print(F.ids["questionsbox"].children[0].text)
                F.ids["questionsbox"].height += 120


            self.sm.current = "Form"
        except Exception as e:
            print(e)



    def build(self):
        self.MS = MainScreen(name="MainScreen", APP = self)
        self.DS = Day(name="Day", APP = self)
        self.ES = NEWEVENT(name="NEWEVENT", APP = self)
        self.F = Form(name = "Form", APP = self)
        self.P = Profile(name="Profile", APP = self)
        self.R = Reg(name="Reg", APP = self)
        self.RS = RateScreen(name="RateScreen", APP = self)
        self.TS = TaskScreen(name="TaskScreen", APP = self)
        self.NTS = NewTaskScreen(name="NewTaskScreen", APP = self)
        self.STS = SubTaskScreen(name="SubTaskScreen", APP = self)
        self.SS = SettingScreen(name="SettingScreen", APP=self)
        self.ST = StatScreen(name="StatScreen", APP=self)

        self.sm = ScreenManager()

        self.sm.add_widget(self.MS)
        self.sm.add_widget(self.DS)
        self.sm.add_widget(self.ES)
        self.sm.add_widget(self.F)
        self.sm.add_widget(self.P)
        self.sm.add_widget(self.R)
        self.sm.add_widget(self.RS)
        self.sm.add_widget(self.TS)
        self.sm.add_widget(self.NTS)
        self.sm.add_widget(self.STS)
        self.sm.add_widget(self.SS)
        self.sm.add_widget(self.ST)

        if not(self.Logic.loaded):
            self.R.show()
        else:
            self.MS.show()


        return self.sm


