from assistant.keyboard import *
from assistant.voice import *
from assistant.utils.intro import intro
from assistant.apis.gpt3 import *
from assistant.apis.wolfram_api import ask_wolfram
from assistant.apis.wikipedia_api import ask_wikipedia
import time
import datetime
import pywhatkit as kit

# COMMENT OLD SKILLS OUT FOR NOW
# # functions for each skill
# def weather(*args):
#   return 'the weather today is sunny with a high of 69 degrees'

# def get_date(*args):
#   t = datetime.datetime.now()
#   day = t.strftime("%A")

#   date = t.strftime("%d")
#   month = t.strftime("%B")
#   year = t.strftime("%Y")

#   return 'its {}, {} {}, {}'.format(day, month, date, year)

# def get_time(*args):
#   t = datetime.datetime.now()
#   hour = t.strftime("%H")
#   minute = t.strftime("%M")
#   ampm = t.strftime("%p")

#   hour = int(hour) % 12

#   return 'its {} {} {}'.format(hour, minute, ampm)

# def get_day(*args):
#   return 'its taco tuesday'


# def quit_app(*args):
#   quit()

# def mouse_mode(*args):
#   mouse_control()

# def introduction(*args):
#   return '''
#           Hello, my name is Dexter. It sure is great to meet you.
#           I am your intelligent assistant, and I am here to help you.
#           '''

# def are_u_up(*args):
#   return 'For you sir, always.'


# def bye(*args):
#   return 'see you later, bitches'

# skills_map = {
#         'introduce': introduction,
#         'are you up': are_u_up, 
#         'time': get_time,
#         'date': get_date,
#         'day': get_day,
#         'quit': quit_app,
#         'mouse': mouse_mode,
#         'track': object_tracker,
#         'menu': open_windows_menu,
#         'file explorer': open_file_explorer,
#         'settings': open_settings,
#         'minimize': minimize,
#         'restore': restore_windows,
#         'task view': task_view,
#         'maximize': maximize_current_window,
#         'search': search,
#         'pause': playpause,
#         'play': playpause,
#         'bye': bye,
#         'sleep': sleep,
#         'shut down': shutdown,
#         'reset': reset,
#         'type': type_mode,
#         'new line': newline,
#        }

# NEW SKILLS


# every skill needs to get passed a query and context parameter


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
    

def question(query, context):
    ans = gpt3_answer(query)
    return ans