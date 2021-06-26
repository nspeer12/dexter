from assistant.keyboard import *
from assistant.voice import *
from assistant.utils.intro import intro
from assistant.apis.gpt3 import *
from assistant.apis.wolfram_api import ask_wolfram
from assistant.apis.wikipedia_api import ask_wikipedia
from assistant.apis.bitcoin import bitcoin_price
from assistant.apis.weather_api import weather_get


import time
import datetime
import pywhatkit as kit
import json
import requests


def greeting(query, context):
    ans = "Hi, I'm Dexter. How can I help you today?"
    return ans

def introduction(query, context):
    ans = 'I am Dexter, your intelligent assistant'
    return ans


def goodbye(query, context):
    ans = 'Goodbye, sir'
    return ans

def wiki(query, context):
    ans = ask_wikipedia(query)
    return ans

def math(query, context):
    ans = ask_wolfram(query)
    return ans

def news(query, context):
    ans = "making api call to top stories from reddit"

def play(query, context):
    song = query.replace("play ", "")
    kit.playonyt(str(song))
    return 'playing ' + str(song)

def resume(query, context):
    # use WinRT api in the future
    pyautogui.press('playpause')
    return None

def pause(query, context):
    # use WinRT api in the future
    pyautogui.press('playpause')
    return None

def increaseVolume(query, context):
    pyautogui.press('volumeup')
    return None

def decreaseVolume(query, context):
    pyautogui.press('volumedown')
    return None

def mute(query, context):
    # differentiate between unmute using sound api
    pyautogui.press('volumemute')
    return None

def unmute(query, context):
    # differentiate between mute using sound api
    pyautogui.press('volumemute')
    return None

def reset(query, context):
    pyautogui.hotkey('win', 'x')
    time.sleep(.1)
    pyautogui.press('u')
    time.sleep(.1)
    pyautogui.press('r')
    return None

def shutdown(query, context):
    pyautogui.hotkey('win', 'x')
    time.sleep(.1)
    pyautogui.press('u')
    time.sleep(.1)
    pyautogui.press('u')
    return None

def sleep(query, context):
    pyautogui.hotkey('win', 'x')
    time.sleep(1)
    pyautogui.press('u')
    time.sleep(1)
    pyautogui.press('s')
    return None

def minimize(query, context):
    pyautogui.hotkey('win', 'm')
    return None

def maximize(query, context):
    pyautogui.hotkey('win', 'up')
    return None

def restore(query, context):
    pyautogui.hotkey('win', 'shiftleft', 'm')
    return None

def switchApplications(query, context):
    pyautogui.hotkey('alt', 'tab')
    return None

def switchDesktop(query, context):
    pyautogui.hotkey('win', 'tab')
    return None

def openApplication(query, context):
    voice("opening Application")
    return None

def openFile(query, context):
    voice("opening file")
    return None

def date(query, context):
    t = datetime.datetime.now()
    day = t.strftime("%A")
    date = t.strftime("%d")
    month = t.strftime("%B")
    year = t.strftime("%Y")

    ans = 'its {}, {} {}, {}'.format(day, month, date, year)
    return ans

def get_time(query, context):
    t = datetime.datetime.now()
    hour = t.strftime("%H")
    minute = t.strftime("%M")
    ampm = t.strftime("%p")
    hour = int(hour) % 12
    ans = 'its {} {} {}'.format(hour, minute, ampm)
    return ans

def day(query, context):
    day_idx = datetime.datetime.today().weekday()
    
    days = {0 : 'monday',
            1 : 'tuesday',
            2 : 'wednesday',
            3 : 'thursday',
            4 : 'friday',
            5 : 'saturday',
            6 : 'sunday'}

    ans = 'today its ' + days[day_idx]
    return ans
    

def question(query:str, context):
    ans = gpt3_answer(query)
    return ans

def convo(query:str, context):
    ans = gpt3_convo(query, context)
    return ans


def print_chat_log(query:str, context):
    print(context)
    return 'here you go sir'

def weather(query, context):
    ans = weather_get(query,"Orlando")
    return ans

