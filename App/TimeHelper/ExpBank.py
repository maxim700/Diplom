from numpy import random
from difflib import SequenceMatcher
import json
import time
class expline:
    def __init__(self,id = None, key = "", priority=0.0, data = None, cost= 0.0, action = 0):
        if id is None:
            self.id = f"expl{time.time()}"
        else:
            self.id = id
        self.key = key#мб будет float#Результат хэш функции параметров
        self.data = data#Набор данны, фактически - распредление тегов в течении недели
        self.action = action
        self.priority = priority  # Приоритет записи в банке опыта
        self.cost = cost# Цена (награда) данного набора

    def tuple(self):
        return (self.key,  self.data, self.action, self.priority, self.cost)

    def dickt(self):
        return (self.id, self.key, self.data, self.action, self.priority, self.cost)

class ExpBank:

    def __init__(self):
        self.bank = {
        }

    def add_exp(self, exp):
        if exp.key in self.bank.keys():
            self.bank[exp.key].append(exp)
        else:
            self.bank[exp.key] = [exp]
        print(self.bank.keys())

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
        #todo было бы классно сделать для поиска дерево
        target = None
        if key in self.bank.keys():
            vars = self.bank[key]
            proc = 0
            for item in vars:
                count = 0
                for i in range(len(data)):
                    if data[i] is None:
                        if item.data[i] is None:
                            count +=1
                    else:
                        if not(item.data[i] is None):
                            count += SequenceMatcher(None, data[i], item.data[i]).ratio()

                count = count/len(data)
                print(f"count {count}")
                if count>proc and count>eps:
                    proc = count
                    target = item
        return target

    def load(self):
        try:
            with open("data_file.json", "r") as file:
                data = json.load(file)
                self.bank = {}
                for key in data.keys():
                    self.bank[key] = []
                    for exp in data[key]:
                        e = expline(id = exp["id"], key = exp["key"], priority=exp["priority"], data = exp["data"], cost= exp["cost"], action = exp["acton"])
                        self.bank[key].append(e)
            file.close()
            return True
        except Exception as e:
            print(e)
            return False


    def save(self):
        with open("data_file.json", "w") as file:
            data = {}
            for key in self.bank.keys():
                data[key] = []
                for exp in self.bank[key]:
                    data[key].append(exp.dickt())
            json.dump(data,file)
        file.close()

    def get(self, key, id):
        print(f"get exp {key} {id}")
        for item in self.bank[key]:
            if item.id == id:
                return item
        return None
