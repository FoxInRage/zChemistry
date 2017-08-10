#data[0] - num - Номер в таблице
#data[1] - name - Имя в таблице
#data[2] - Rname - Русское название
#data[3] - Lname - Латинское название
#data[4] - Ename - Английское название
#data[5] - Birth - Дата открытия
#data[6] - Eshell - Электронная оболочка
#data[7] - Doxi - Степень окисления
#data[8] - Amass - Атомная масса
#data[9] - density - Плотность
#data[10] - Tmelting - Температура плавления
#data[11] - boil - Температура кипения

import flask
import logging
import telebot
import time
import os
import sqlite3
import finder
import keygen
from finder import elements_1
from OpenSSL import SSL
from telebot import types

os.chdir('/root/to/main.py')

class temps:
    onely = False
    sa = False
    search = False
    dR = True



TOKEN = 'Your Token'
WEBHOOK_HOST = 'Your Host'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr
WEBHOOK_SSL_CERT = '/root/to/ssl/cert'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = '/root/to/ssl/priv' # Path to the ssl private key
WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (TOKEN)


logger = telebot.logger

telebot.logger.setLevel(logging.INFO)


bot = telebot.TeleBot(TOKEN)


app = flask.Flask(__name__)



# Empty webserver index, return nothing, just http 200

@app.route('/', methods=['GET']) 
def index(): 
    return 'Test'


# Process webhook calls

@app.route(WEBHOOK_URL_PATH, methods=['POST'])

def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ' '





rate = []

admin = [219533807, 389810246, 343980577, 185091202]

data = {}

markup=types.ReplyKeyboardMarkup(resize_keyboard=True)


bot = telebot.TeleBot(TOKEN)
      
@bot.message_handler(commands=['start','help'])
def start(message):
       id = message.from_user.id
       if temps.onely == False:
           markup.add("Поиск🔎")
           markup.add("О боте")
           markup.add("Контакты📖")
           temps.onely = True
           bot.send_message(message.chat.id, "Добро пожаловать! следи за ходом разработки на канале @zChemistryBlog, если есть вопросы или хочешь узнать дополнительные возможности? заходи сюда - @zChemistryGroup",reply_markup=markup)
       else:
           if message.from_user.username == None:
              username = 'Нету'
           else:
               username = '@'+message.from_user.username
           text = 'Новый юзер!\n'+'Первое имя: ' + message.from_user.first_name+'\nЮзернейм: ' + username
           for x in range(0, len(admin)):
              bot.send_message(admin[x], text)
           bot.send_message(message.chat.id, "Добро пожаловать! следи за ходом разработки на канале @zChemistryBlog, если есть вопросы или хочешь узнать дополнительные возможности? заходи сюда - @zChemistryGroup",reply_markup=markup)


@bot.message_handler(commands=['myid'])
def whid(message):
      id = message.from_user.id
      bot.send_message(message.chat.id, id)

@bot.inline_handler(lambda query: len(query.query)>0)
def query_text(query):
    try:
        data = {}
        choice = query.query
        data = finder.find(choice)
        desc = 'Поиск: ' + data["name"]
        text = 'Поиск по: '+query.query+'\n\n*'+str(data["name"]) + ' (' + str(data["num"])+ ' номер в таблице)\n'+'*'+'Русское название: ' + '*'+ data["Rname"] + '*'+'\nЛатинское название: ' + '*'+data["Lname"]+'*' +'\nАнглийское название: ' +'*'+ data["Ename"]+'*' +'\nДата открытия: ' + '*' + str(data["Birth"]) +'*'+'\nЭлектронная оболочка: ' + '*'+data["Eshell"] +'*'+'\nСтепень окисления: ' + '*' +data["Doxi"]+'*' +'\nАтомная масса: ' +'*'+ data["Amass"] +' (г/моль)'+'*'+'\nПлотность: ' + '*'+data["density"] + ' (г/см³)'+'*'+'\nТемпература плавления: ' + '*'+data["Tmelting"] + '°C' +'*'+'\nТемпература кипения: ' + '*'+data["boil"] + '°C'+'*'
        r = types.InlineQueryResultArticle('1', desc, types.InputTextMessageContent(text, parse_mode="MARKDOWN"))
        bot.answer_inline_query(query.id, [r])
        rate.append(data["name"])
    except:
            er = 'Поиск по: ' + query.query + '\n\nЭлемент не найден!'
            r2 = types.InlineQueryResultArticle(
            	    '2', title='Ошибка!',
            	    description='Элемент не найден!',
            	    input_message_content=types.InputTextMessageContent(er))
            bot.answer_inline_query(query.id, [r2])

@bot.message_handler(commands=['generate'])
def runKeyGen(message):
      id = message.from_user.id
      if id in admin:
          num = int(message.text.split(' ')[1])
          len = int(message.text.split(' ')[2])
          key = keygen.keyGenerator(len,num)
          bot.send_message(message.chat.id, key)    
      else:
          bot.send_message(message.chat.id, 'Нет полномочий!')

@bot.message_handler(commands=["rate"])
def rater(message):
     if message.from_user.id in admin:
        x = message.text.split(' ')[1]
        if x == 777:
            bot.send_message(message.chat.id, rate)
        data = finder.find(x)
        if data == None:
           bot.send_message(message.chat.id, 'Такого элемента нет')
        else:
           y = rate.count(data["name"])
           text = data["name"] + ' - искалось ' + str(y) + ' раз'
           bot.send_message(message.chat.id, text)
     else:
        bot.send_message(message.chat.id, 'Вы не уполномочены!')
 
@bot.message_handler(commands=["send"])
def sendAdmin(message):
    if message.from_user.id in admin:
        bot.send_message(message.chat.id, 'Ваш текст: ')
        temps.sa = True
    else:
        bot.send_message(message.chat.id, 'Вы не уполномоченны')
      
@bot.message_handler(content_types=["text"])
def checkC(message):
      if message.text == 'Поиск🔎':
            bot.send_message(message.chat.id,'Введите Элемент: ')
            temps.search = True
              
      elif message.text == 'О боте':
             if temps.search == True:
                 bot.send_message(message.chat.id, 'Поиск отменен!')
             bot.send_message(message.chat.id, 'Помощник по Химии, с большой базой данных по химическим элементам - присоединяйся к каналу и узнавай первые новости по ходу разработки бота @zChemistryBlog')
             temps.search = False  
      
      elif message.text == 'Контакты📖':
              if temps.search == True:
                 bot.send_message(message.chat.id, 'Поиск отменен!')
              text = 'Группы: '+'<a href="https://t.me/joinchat/FzwIRkMaeoC3OjD2rGz_eg">Общая zChemistry</a>'+'\n'+'Каналы: '+'<a href="t.me/zChemistryBlog">Блог Разработчика</a>'+'\n'+'Спасибо: '+'<a href="https://t.me/chatdmbot?start=shyrcoep7758">ChatDM</a>'
              bot.send_message(message.chat.id, text, parse_mode="HTML", disable_web_page_preview=True)
              
      elif temps.search == True:
              temps.search = False
              finds(message)
              
      elif temps.sa == True:
           temps.sa = False
           for x in range(0, len(admin)):
              bot.send_message(admin[x], message.text)
                           
def finds(message):     
          keyboard=types.InlineKeyboardMarkup()
          rateMe = types.InlineKeyboardButton(text="Оценить!", url="https://telegram.me/storebot?start=zChemistryBot")
          joinG = types.InlineKeyboardButton(text='Группа!', url="t.me/zChemistryGroup")
          joinB = types.InlineKeyboardButton(text='Канал!', url ="t.me/zChemistryBlog")
          keyboard.add(rateMe, joinG, joinB)

          choice = message.text
          data = finder.find(choice)
          if data == None:
             text = 'Такого не существует!'
             bot.send_message(message.chat.id, text)
          
          else:
             rate.append(data["name"])
             try: 
                photo = open(elements_1[choice]['/home/zchemistry/Chem/'+data["link"]], 'rb')
                bot.send_photo(message.chat.id, photo)
                photo.close()
             except Exception as error:
               print(error)
             text = '*'+str(data["name"]) + ' (' + str(data["num"])+ ' номер в таблице)\n'+'*'+'Русское название: ' + '*'+ data["Rname"] + '*'+'\nЛатинское название: ' + '*'+data["Lname"]+'*' +'\nАнглийское название: ' +'*'+ data["Ename"]+'*' +'\nДата открытия: ' + '*' + str(data["Birth"]) +'*'+'\nЭлектронная оболочка: ' + '*'+data["Eshell"] +'*'+'\nСтепень окисления: ' + '*' +data["Doxi"]+'*' +'\nАтомная масса: ' +'*'+ data["Amass"] +' (г/моль)'+'*'+'\nПлотность: ' + '*'+data["density"] + ' (г/см³)'+'*'+'\nТемпература плавления: ' + '*'+data["Tmelting"] + '°C' +'*'+'\nТемпература кипения: ' + '*'+data["boil"] + '°C'+'*'
             bot.send_message(message.chat.id, text, parse_mode="MARKDOWN")
             bot.send_message(message.chat.id, 'Понравилось? ставь самую высокую оценку.\nА также присоединяйся к нам!',reply_markup=keyboard,disable_web_page_preview=True)
     

bot.remove_webhook()


# Set webhook

bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH, certificate=open(WEBHOOK_SSL_CERT, 'r'))


# Start flask server
if __name__ == '__main__':
    app.run(host=WEBHOOK_LISTEN, port=WEBHOOK_PORT, ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV), debug=True)


