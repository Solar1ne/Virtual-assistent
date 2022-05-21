import datetime
import os
import random
import requests
import pyttsx3
import speech_recognition as sr
from datetime import date
from fuzzywuzzy import fuzz
from time import sleep
import pygame

opts = {
    'names': ('гарик', 'гар', 'бро'),
    'tbr': ('скажи', 'вруби', 'намути', 'сколько', 'какой', 'какое', 'какая', 'добавь', 'поставь', 'посчитай', 'мне'),
    'cmds': {
        'greeting': ('привет', 'привет друг', 'салам', 'приветики', 'хаюшки', 'хай', 'здорово', 'здорова'),
        'create_task': ('задачку', 'у меня тут дельце появилось'),
        'dating': ('сегодня число', 'число'),
        'timing': ('который час', 'времени', 'время'),
        'weekday': ('сегодня день недели', 'день недели'),
        'timer': ('таймер', 'засеки время'),
        'weather': ('что по погоде', 'погода'),
        'factorial': ('факториал', 'факториал'),
        'playMusic': ('музыку', 'музон', 'музяка', 'трек'),
        'yesorno': ('да или нет', 'нет или да'),
        'support': ('страшно', 'волнуюсь', 'скоро сессия'),
        'timetable': ('расписание', 'пары'),
        'end': ('пока', 'до свидания', 'алибидерчи')
    }
}


def callback():
    try:
        with m as mic:
            r.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = r.listen(source=mic)
            voice = r.recognize_google(audio_data=audio, language='ru-RU').lower()
        print('Распознано: ' + voice)

        if voice.startswith(opts['names']):
            cmd = voice

            for x in opts['names']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

        else:
            return voice

    except sr.UnknownValueError:
        print('Голос не распознан!')


def listenEN():
    try:
        with m as mic:
            r.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = r.listen(source=mic)
            return r.recognize_google(audio_data=audio, language='en-EN').lower()
    except sr.UnknownValueError:
        pass


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    if cmd == 'greeting':
        greeting()
    elif cmd == 'create_task':
        create_task()
    elif cmd == 'dating':
        dating()
    elif cmd == 'timing':
        timing()
    elif cmd == 'weekday':
        weekday()
    elif cmd == 'timer':
        timer()
    elif cmd == 'weather':
        weather()
    elif cmd == 'factorial':
        factorial()
    elif cmd == 'playMusic':
        playMusic()
    elif cmd == 'yesorno':
        yesorno()
    elif cmd == 'support':
        support()
    elif cmd == 'timetable':
        timetable()
    elif cmd == 'end':
        speak('рад помочь, до свидания')
    else:
        unclear()


def speak(speech):
    speak_engine.say(speech)
    speak_engine.runAndWait()
    speak_engine.stop()


def greeting():
    speak('Приветствую хозяин')


def create_task():
    speak('Что добавим в список дел?')
    task = callback()
    with open('todo-list.txt', 'a') as file:
        file.write(f'{task}\n')
    speak(f'Задача "{task}" успешно добавлена')


def dating():
    today = date.today()
    speak(f'Сегодня {today}')


def timing():
    dt = datetime.datetime.now()
    today = dt.time()
    correct = {0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09'}
    hours = today.hour
    minutes = today.minute
    seconds = today.second
    if today.hour < 10:
        hours = correct[today.hour]
    if today.minute < 10:
        minutes = correct[today.minute]
    if today.second < 10:
        seconds = correct[today.second]
    speak(f'Сейчас {hours}:{minutes}:{seconds}')


def weekday():
    dt = datetime.datetime.now()
    wd = {0: 'понедельник', 1: 'вторник', 2: 'среда', 3: 'четверг', 4: 'пятница', 5: 'суббота', 6: 'воскресенье'}
    today = wd[dt.weekday()]
    speak(f'Сегодня {today}')


def timer():
    speak('На сколько секунд поставить таймер?')
    seconds = callback()
    try:
        s = int(seconds)
        speak('Время пошло!!!')
        sleep(s / 2)
        if s > 5:
            speak('Осталась половина')
        sleep((s / 2) - 1)
        os.system(r'C:\Users\Admin\PycharmProjects\VoiceAssistent\timerring.mp3')
        speak('Время вышло!!!')
    except ValueError:
        speak('Не понялa Вас')
    except TypeError:
        speak('Не понялa Вас')


def weather():
    speak('В каком городе Вы хотите узнать погоду?')
    city = callback()
    cts = {'москва': 'Moscow', 'нахабино': 'Nakhabino', 'санкт-петербург': 'Saint Petersburg', 'волгоград': 'Volgograd',
           'сочи': 'Sochi', 'омск': 'Omsk', 'чита': 'Chita'}
    city = cts[city]
    loc = f'{city},RU'
    req = requests.get("http://api.openweathermap.org/data/2.5/weather",
                       params={'q': f'{loc}', 'units': 'metric', 'lang': 'ru',
                               'APPID': '4b40bec5212b532c48066246c26cb887'}).json()

    temp = str(int(req['main']['temp']))
    end = temp[-1]
    ends = {0: '0 градусов', 1: '1 градус', 2: '2 градусa', 3: '3 градуса', 4: '4 градуса'}
    if -1 < int(end) < 5:
        temp = ends[int(end)]
    else:
        temp = end + ' градусов'
    press = int((req['main']['pressure']) * 0.75188)

    desc = req['weather'][0]['description']
    hum = req['main']['humidity']

    rc = {'Moscow': 'Москве',
          'Nakhabino': 'Нахабино',
          'Saint Petersburg': 'Санкт-Петербурге',
          'Volgograd': 'Волгограде',
          'Sochi': 'Сочи',
          'Omsk': 'Омске',
          'Chita': 'Чите'}
    city = rc[city]

    speak(f'В {city} {desc}, {temp}, давление: {press}, влажность: {hum}%')


def factorial():
    speak('Факториал какого числа Вы хотите посчитать?')
    n = str(callback())
    try:
        k = int(n)
    except ValueError:
        return 'Я ожидал натуральное число('
    f = 1
    for i in range(2, k + 1):
        f = f * i
    speak(f'{f}')


def yesorno():
    a = random.randint(0, 1)
    if a == 0:
        speak('Да!')
    else:
        speak('Нет!')


def playMusic():
    speak('Какую песню включить?')
    song = listenEN()
    speak('Наслаждайтесь')
    path = "C:\\Users\\Admin\\PycharmProjects\\VoiceAssistent\\Music\\" + f"{song}" + ".mp3"
    os.system(path)


def support():
    speak('Конечно, студенческая жизнь тяжела, но многие через это проходят. У вас тоже всё получится!')


def timetable():
    timetable = {'понедельник': 'второй парой Физика, третьей дискретная математика, четвертой основы программирования и пятой проектная практика',
                 'вторник': 'первой парой основы программирования, второй история, третьей физкультура и четвёртой линейная алгебра',
                 'среда': 'дистанционный день. вторая пара английский, третья математический анализ, четвёртая теория графов и пятой основы программирования',
                 'четверг': 'первой и третьей парой математический анализ, второй общая алгебра, четвёртой английский и пятой физкультура',
                 'пятница': 'дистанционный день. первой и второй парой общая алгебра, третьей физика, четвёртой история и пятая линейная алгебра',
                 'суббота': 'ура пар нет',
                 'воскресенье': 'ура пар нет'}
    speak('в какой день вы хотите узнать расписание?')
    dw = callback()
    speak(timetable[dw])


def unclear():
    speak('Простите: не понимаю Вас')


r = sr.Recognizer()
m = sr.Microphone()

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

pygame.init()
pygame.display.set_caption('Image')
img = pygame.image.load("background.jpg")
img = pygame.transform.scale(img, (1920, 1080))
display = pygame.display.set_mode((1920, 1080))
display.blit(img, [0, 0])
pygame.display.update()
speak('Я родился')
speak('Гарик слушает')

while True:
    callback()
    sleep(0.1)