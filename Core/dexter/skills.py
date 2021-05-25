import time
import datetime
from mouse import *
from track import object_tracker
from keyboard import *
from intro import intro
import pywhatkit as kit
from voice import *
from gpt3 import *


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


def greeting(self, query, context):
    voice("greeting")

def introduction(self, query, context):
    voice("I am Dexter")

def goodbye(self, query, context):
    voice("goodbye")

def wiki(self, query, context):
    voice("making api call to wiki")

def math(self, query, context):
    voice("making api call to wolf frame alpha")

def news(self, query, context):
    voice("making api call to top stories from reddit")

def play(self, query, context):
    voice(message.replace("play", "playing"))
    song = message.replace("play ", "")
    kit.playonyt(str(song))

def resume(self, query, context):
    # use WinRT api in the future
    pyautogui.press('playpause')

def pause(self, query, context):
    # use WinRT api in the future
    pyautogui.press('playpause')

def increaseVolume(self, query, context):
    pyautogui.press('volumeup')

def decreaseVolume(self, query, context):
    pyautogui.press('volumedown')

def mute(self, query, context):
    # differentiate between unmute using sound api
    pyautogui.press('volumemute')

def unmute(self, query, context):
    # differentiate between mute using sound api
    pyautogui.press('volumemute')

def reset(self, query, context):
	pyautogui.hotkey('win', 'x')
	time.sleep(.1)
	pyautogui.press('u')
	time.sleep(.1)
	pyautogui.press('r')

def shutdown(self, query, context):
	pyautogui.hotkey('win', 'x')
	time.sleep(.1)
	pyautogui.press('u')
	time.sleep(.1)
	pyautogui.press('u')

def sleep(self, query, context):
	pyautogui.hotkey('win', 'x')
	time.sleep(1)
	pyautogui.press('u')
	time.sleep(1)
	pyautogui.press('s')

def minimize(self, query, context):
    pyautogui.hotkey('win', 'm')

def maximize(self, query, context):
    pyautogui.hotkey('win', 'up')

def restore(self, query, context):
    pyautogui.hotkey('win', 'shiftleft', 'm')

def switchApplications(self, query, context):
    pyautogui.hotkey('alt', 'tab')

def switchDesktop(self, query, context):
    pyautogui.hotkey('win', 'tab')

def openApplication(self, query, context):
    voice("opening Application")

def openFile(self, query, context):
    voice("opening file")

def date(self, query, context):
    t = datetime.datetime.now()
    day = t.strftime("%A")
    date = t.strftime("%d")
    month = t.strftime("%B")
    year = t.strftime("%Y")

    voice('its {}, {} {}, {}'.format(day, month, date, year))

def get_time(self, query, context):
    t = datetime.datetime.now()
    hour = t.strftime("%H")
    minute = t.strftime("%M")
    ampm = t.strftime("%p")
    hour = int(hour) % 12
    voice('its {} {} {}'.format(hour, minute, ampm))

def day(self, query, context):
    voice(self,"it taco tuesday")

def question(self, query, context):
    print('here')
    voice(gpt3_answer(query))