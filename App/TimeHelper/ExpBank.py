from numpy import random
from difflib import SequenceMatcher
class expline:
    def __init__(self, key="", priority=0.0, data = None, cost= 0.0, action = 0):
        self.key = key#мб будет float#Результат хэш функции параметров
        self.priority = priority#Приоритет записи в банке опыта
        self.data = data#Набор данны, фактически - распредление тегов в течении недели
        self.cost = cost# Цена (награда) данного набора
        self.action = action



    def tuple(self):
        return (self.key, self.priority, self.data, self.cost, self.action)

class ExpBank:

    def __init__(self):
        self.bank = {
        }

    def add_exp(self, exp):
        if exp.key in self.bank.keys():
            self.bank[exp.key].append(exp)
        else:
            self.bank[exp.key] = [exp]


    #todo функция очистки от ненужных записей?
    #todo save
    #todo load
    #



    def get_exp(self, key):
        '''
        Возвразает один из 3х наиболее приоритетных набороы для данного ключа
        '''
        if key in self.bank.keys():
            prioritiet = sorted(self.bank[key],key = lambda x: x.priority, reverse=True)
            if len(prioritiet)>3:
                #prioritiet = list(map(tuple,prioritiet[:3]))
                prioritiet = prioritiet[:3]

            return prioritiet[random.randint(len(prioritiet))]
        else:
            return None


    def find(self,key, data, eps = 0.5):
        target = None
        if key in self.bank.keys():
            vars = self.bank[key]

            proc = 0
            for item in vars:
                count = 0
                for i in range(32):
                    if not(item[i] is None) and not(data[i] is None):
                        count += SequenceMatcher(None, item[i], data[i]).ratio()
                if count>proc and count>eps:
                    proc = count
                    target = item
        return target

a1 = expline("a",0.5, ["1"], 0.4, 3)
a2 = expline("a",0.3, ["2"], 0.4, 3)
a3 = expline("a",0.7, ["3"], 0.4, 3)
a4 = expline("a",0.8, ["4"], 0.4, 3)
B = ExpBank()
B.add_exp(a1)
B.add_exp(a2)
B.add_exp(a3)
B.add_exp(a4)
print(list(B.bank.keys()))
print(B.get_exp("a"))