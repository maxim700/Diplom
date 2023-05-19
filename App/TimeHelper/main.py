from Calendar import *
from Brain import *
from ExpBank import *

#Тест
C = calendar()
ev = Event.event("30.04.2023","21:30", {"name":"test1","duration":100,"Friend":True})
print(ev)
ev1 = Event.event("30.04.2023","22:00", {"name":"test2","Activ":True, "Friends":True, "Road":True})
ev2 = Event.event("30.04.2023","20:30", {"name":"test2","Activ":True, "Friends":True, "Road":True})
ev3 = Event.event("30.04.2023","12:27", {"name":"test2","Activ":True, "Friends":True, "Road":True})
ev4 = Event.event("30.04.2023","15:40", {"name":"test2","Activ":True, "Friends":True, "Road":True})
ev5 = Event.event("30.04.2023","22:30", {"name":"test2","Activ":True, "Friends":True, "Road":True})
ev6 = Event.event("01.05.2023","22:31", {"name":"test2","duration":30,"Friend":True,"Road":True})
ev7 = Event.event("04.05.2023","22:30", {"name":"test3","duration":30,"Relax":True})
C.add_event(ev)
C.add_event(ev1)
C.add_event(ev2)
C.add_event(ev3)
C.add_event(ev4)
C.add_event(ev5)
C.add_event(ev6)
C.add_event(ev7)
C.save()
# print(C.dates)
# C.remove_event("12.02.2023","22:30", "test1")
#C.load()
print(C.dates)

print("_______________")
data = C.get_period((4,5,2023),(9,5,2023))
print(len(data))
for i in data:
    print(i)
state = C.format(data)
print(f"state:\n{state}")
print(len(C.format(data)))
#
Bank = ExpBank()
optimazer = Adam(learning_rate=0.01)
Brain = Agent(C, optimazer, Bank, "test")
Brain._build_compile_model()
action = Brain.act("test",state)
print(f"Рекоендация {action}")
#
