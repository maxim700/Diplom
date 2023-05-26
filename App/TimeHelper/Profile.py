import json
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
            "responsibility": None,
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
        with open("profile.json", "w") as file:
            json.dump(self.skills, file)
        file.close()

    def load(self):
        try:
            with open("profile.json", "r") as file:
                self.skills = json.load(file)
            file.close()
            return True
        except Exception as e:
            print(e)
            return False

    def key(self):
        res = ""
        for skill in self.skills:
            print(self.skills[skill])
            match self.skills[skill]:
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
