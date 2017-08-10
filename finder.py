#num - Номер в таблице
#name - Имя в таблице
#Lname - Латинское название
#Ename - Английское название
#Birth - Дата открытия
#Eshell - Электронная оболочка
#Doxi - Степень окисления
#Amass - Атомная масса
#density - Плотность
#Tmelting - Температура плавления
#Boil - Температура кипения

from chem import elements_1

elem = {
    'num',
    'name',
    'Rname',
    'Lname',
    'Ename',
    'Birth',
    'Eshell',
    'Doxi',
    'Amass',
    'density',
    'Tmelting',
    'boil'
}


def find(choice):
   try:
      try:
        if int(choice) > 118 or int(choice) < 1:
            return None
        data = {}
        choice = [i for i in elements_1 if elements_1[i]["num"] == int(choice)][0]
        for i in elem:
            data[i] = elements_1[choice][i]
        return data

      except ValueError:
        data = {}
        for i in elements_1:
            if elements_1[i]["name"] == choice:
                choice = i
            else:
                ch = choice.title()
                if elements_1[i]["name"] == ch:
                   choice = i
        for i in elem:
            data[i] = elements_1[choice][i]
        return data
        
   except KeyError:
      try:
          ch = choice.title()
          data = {}
          for i in elements_1:
            if elements_1[i]["Rname"] == choice:
                choice = i
            else:
                if elements_1[i]["Rname"] == ch:
                       choice = i
                else:
                   if elements_1[i]["Ename"] == choice:
                        choice = i
                   elif elements_1[i]["Ename"] == ch:
                         choice = i
          for i in elem:
            data[i] = elements_1[choice][i]
          return data
              
      except KeyError:
           return None
