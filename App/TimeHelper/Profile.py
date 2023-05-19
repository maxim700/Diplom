#Библиотека для гугл аккаунта + вопрос на разрешение!!!!

class prof:

    def __init__(self):
        '''
        Класс для работы с параметрами пользователя
        Парметры представляют собой словарь {название: значение(float)}
        '''
        self.skills = {
            "people": None,
            "noize": None,
            "job": None,
            "sleep": None,
            "activ": None,
            "road": None,
            "multiwork": None,
            "stress": None,
            "resp": None,
            "plan": None,
            "motivation": None,
            "hobby": None
        }
        self.keys = list(self.skills.keys())

    def set_skills(self, skills):
        for i, skill in enumerate(skills):
            self.skills[self.keys[i]] = skill

    def change_skills(self, skills):
        if self.skills[self.keys[0]] != None:
            for i, skill in enumerate(skills):
                self.skills[self.keys[i]] += skill
        else:
            self.set_skills(skills)

    def save(self):
        file = open("profsave.txt", 'w')
        for i,skill in enumerate(self.skills):
            file.write(f"{skill},{self.skills[skill]}\n")
        file.close()

    def load(self):
        file = open("profsave.txt", 'r')
        for i, skill in enumerate(self.skills):
            s = file.readline().split(',')
            self.skills[s[0]] = float(s[1])
        file.close()

    def key(self):
        res = ""
        for skill in self.skills:
            match skill:
                case 1 | 2:
                    res += "A"
                case 3 | 4 | 5:
                    res += "B"
                case 6 | 7 | 8:
                    res += "C"
                case 9 | 10:
                    res += "D"
        return res

#тест
# p1 = prof()
# p1.set_skills((1,2))
# p1.save()
# p1.set_skills((3,4))
# p1.load()
# print(p1.skills)
