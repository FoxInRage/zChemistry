import random

def keyGenerator(len, num):
    text = 'After Generate: \n\n'
    str1 = '123456789-'
    str2 = 'qwertyuiopasdfghjklzxcvbnm-'
    str3 = str2.upper()
    str4 = str1 + str2 + str3
    ls = list(str4)
    for x in range(num):
        random.shuffle(ls)
        psw = ''.join([random.choice(ls) for x in range(len)])
        text = text + psw + '\n'
    return text
