from numpy import random
from difflib import SequenceMatcher
import json
import time
class expline:
    def __init__(self, key = "", priority=0.0, data = None, cost= 0.0, action = 0):
        self.id = f"expl{time.time}"
        self.key = key#мб будет float#Результат хэш функции параметров
        self.data = data#Набор данны, фактически - распредление тегов в течении недели
        self.action = action
        self.priority = priority  # Приоритет записи в банке опыта
        self.cost = cost# Цена (награда) данного набора

    def tuple(self):
        return (self.key,  self.data, self.action, self.priority, self.cost)

class ExpBank:

    def __init__(self):
        self.bank = {
        }

    def add_exp(self, exp):
        if exp.key in self.bank.keys():
            self.bank[exp.key].append(exp)
        else:
            self.bank[exp.key] = [exp]

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
                for tag in data:
                    #Почекать размеронсть
                    #todo есть баг
                    count = SequenceMatcher(None, data, item.data).ratio()
                if count>proc and count>eps:
                    proc = count
                    target = item
        return target

    def load(self):
        try:
            with open("data_file.json", "r") as file:
                self.bank = json.load(file)
                print(self.bank)
            file.close()
            return True
        except Exception as e:
            print(e)
            return False


    def save(self):
        with open("data_file.json", "w") as file:
            json.dump(self.bank,file)
        file.close()

    def get(self, key, id):
        for item in self.bank[key]:
            if item.id == id:
                return item
        return None
