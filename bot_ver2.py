'''
requests - библиотека позволяет нам легко и с минимальным количеством кода взаимодействовать с веб-приложениями
time - библиотека для работы с системным временем
vk_api - для работы с API ВКонтакте
'''
import datetime #работа с датой
import time #работа с датой
import requests #работа с http страничками
import vk_api #работа с апи вк
import re #для работы с регулярными выражениями

from pyowm import OWM #работа с апи сайта https://openweathermap.org/
owm = OWM('key')  

#подключение к группе ВК
vk_session = vk_api.VkApi(token='d123dfc1d0946ba58a7549c5ac576a0a7bad2636ab3d84b5a0ba1c1ea49d0f3b5a0103ab3bfd62c414a60')
'''
#подключение к личной странице
session = requests.Session()
login, password = 'Ваш логин, email или телефон', 'Ваш пароль'
vk_session = vk_api.VkApi(login, password)
try:
    vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)
    return
'''


from vk_api.longpoll import VkLongPoll, VkEventType
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

def sms (text): #функция отправки сообщения
    vk.messages.send(
        user_id = event.user_id, #id пользователя, которому отвечаем
        message=text,               #текст сообщения
        random_id=time.time()   #это веселый костыль, который нужен для усложнения жизни
        )
def pogoda(sity): #получение погоды с сайта 
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(sity)
    w = observation.weather
    #получаем из списка параметр temp
    #print(w)
    temperature = w.temperature('celsius')['temp']
    #лучаем влажность
    humi = w.humidity
    #формируем строку - ответ
    info = 'В городе '+sity+' сейчас '+str(temperature)+' градусов и '+str(humi)+ ' процентов влажности воздуха'
    return info

def log(user_name,text):
    '''
    Режимы чтения файла
    r - чтение файла
    w - перезаписать файл
        Если файла нет его создадут, если он был то пресоздается
    a - добавление в файл
        Дописывает в файлик данные к существующим
    b - binari mode
        Нужен для чтения медиаконтента
'''
    t = datetime.datetime.now()  
    file = open('log.txt', 'a', encoding="utf-8")
    file.write(str(t)+" "+user_name+" написал: "+text+'\n')
    file.close()
    
#while(True): #проверяем события в группе в бесконечном цикле
for event in longpoll.listen():
    #Слушаем longpoll, если пришло сообщение то:    
    if event.from_user and not (event.from_me) and event.text != None:  #Если написали в ЛС и сообщение не от группы
        #---ловим имя пользователя написавшего нам---
        user_get=vk.users.get(user_ids = (event.user_id))
        user_get=user_get[0]
        first_name=user_get['first_name']
        last_name=user_get['last_name']
        userName=first_name+" "+last_name
        #--------------------------------------------
        user_text = event.text #содержит в себе текст сообщения от пользователя
        #передаем функции имя пользователя и текст сообщения
        #log(userName,user_text)        
        #разбиваем строку на слова
        lst = user_text.replace(' ',' ').split() # в кавычках разделители
        print(lst)
        if lst[0] == "бот":
            if lst[1] == "погода": #проверка содержимого
                if lst[2] != None:
                    try:
                        info = pogoda(lst[2])
                        sms(info) #передаем в функцию отправки сообщения текст сообщения
                    except:
                        sms("ты втирешь мне какую-то дичь")
                else:
                    sms("Не вижу названия города")
          
