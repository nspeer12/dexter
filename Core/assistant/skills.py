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
# 	return 'the weather today is sunny with a high of 69 degrees'

# def get_date(*args):
# 	t = datetime.datetime.now()
# 	day = t.strftime("%A")

# 	date = t.strftime("%d")
# 	month = t.strftime("%B")
# 	year = t.strftime("%Y")

# 	return 'its {}, {} {}, {}'.format(day, month, date, year)

# def get_time(*args):
# 	t = datetime.datetime.now()
# 	hour = t.strftime("%H")
# 	minute = t.strftime("%M")
# 	ampm = t.strftime("%p")

# 	hour = int(hour) % 12

# 	return 'its {} {} {}'.format(hour, minute, ampm)

# def get_day(*args):
# 	return 'its taco tuesday'


# def quit_app(*args):
# 	quit()

# def mouse_mode(*args):
# 	mouse_control()

# def introduction(*args):
# 	return '''
# 			Hello, my name is Dexter. It sure is great to meet you.
# 			I am your intelligent assistant, and I am here to help you.
# 			'''

# def are_u_up(*args):
# 	return 'For you sir, always.'


# def bye(*args):
# 	return 'see you later, bitches'

# skills_map = {
# 		  'introduce': introduction,
# 		  'are you up': are_u_up, 
# 		  'time': get_time,
# 		  'date': get_date,
# 		  'day': get_day,
# 		  'quit': quit_app,
# 		  'mouse': mouse_mode,
# 		  'track': object_tracker,
# 		  'menu': open_windows_menu,
# 		  'file explorer': open_file_explorer,
# 		  'settings': open_settings,
# 		  'minimize': minimize,
# 		  'restore': restore_windows,
# 		  'task view': task_view,
# 		  'maximize': maximize_current_window,
# 		  'search': search,
# 		  'pause': playpause,
# 		  'play': playpause,
# 		  'bye': bye,
# 		  'sleep': sleep,
# 		  'shut down': shutdown,
# 		  'reset': reset,
# 		  'type': type_mode,
# 		  'new line': newline,
# 		 }

# NEW SKILLS


# every skill needs to get passed a query and context parameter


def greeting(query, context):
    voice("Hi, I'm Dexter. How can I help you today?")

def introduction(query, context):
    voice("I am Dexter")

def goodbye(query, context):
    voice("goodbye")

def wiki(query, context):
    text = ask_wikipedia(query)
    voice(text)

def math(query, context):
    text = ask_wolfram(query)
    voice(text)

def news(query, context):
    voice("making api call to top stories from reddit")

def play(query, context):
    voice(query.replace("play", "playing"))
    song = query.replace("play ", "")
    kit.playonyt(str(song))

def resume(query, context):
    # use WinRT api in the future
    pyautogui.press('playpause')

def pause(query, context):
    # use WinRT api in the future
    pyautogui.press('playpause')

def increaseVolume(query, context):
    pyautogui.press('volumeup')

def decreaseVolume(query, context):
    pyautogui.press('volumedown')

def mute(query, context):
    # differentiate between unmute using sound api
    pyautogui.press('volumemute')

def unmute(query, context):
    # differentiate between mute using sound api
    pyautogui.press('volumemute')

def reset(query, context):
	pyautogui.hotkey('win', 'x')
	time.sleep(.1)
	pyautogui.press('u')
	time.sleep(.1)
	pyautogui.press('r')

def shutdown(query, context):
	pyautogui.hotkey('win', 'x')
	time.sleep(.1)
	pyautogui.press('u')
	time.sleep(.1)
	pyautogui.press('u')

def sleep(query, context):
	pyautogui.hotkey('win', 'x')
	time.sleep(1)
	pyautogui.press('u')
	time.sleep(1)
	pyautogui.press('s')

def minimize(query, context):
    pyautogui.hotkey('win', 'm')

def maximize(query, context):
    pyautogui.hotkey('win', 'up')

def restore(query, context):
    pyautogui.hotkey('win', 'shiftleft', 'm')

def switchApplications(query, context):
    pyautogui.hotkey('alt', 'tab')

def switchDesktop(query, context):
    pyautogui.hotkey('win', 'tab')

def openApplication(query, context):
    voice("opening Application")

def openFile(query, context):
    voice("opening file")

def date(query, context):
    t = datetime.datetime.now()
    day = t.strftime("%A")
    date = t.strftime("%d")
    month = t.strftime("%B")
    year = t.strftime("%Y")

    voice('its {}, {} {}, {}'.format(day, month, date, year))

def get_time(query, context):
    t = datetime.datetime.now()
    hour = t.strftime("%H")
    minute = t.strftime("%M")
    ampm = t.strftime("%p")
    hour = int(hour) % 12
    voice('its {} {} {}'.format(hour, minute, ampm))

def day(query, context):
    voice(self,"it taco tuesday")

def question(query, context):
    print('here')
    voice(gpt3_answer(query))