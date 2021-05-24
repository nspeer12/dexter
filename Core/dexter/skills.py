import time
import datetime
from mouse import *
from track import object_tracker
from keyboard import *
from intro import intro
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

def greeting(self):
    voice("greeting")

def introduction(self):
    voice("I am Dexter")

def goodbye(self):
    voice("goodbye")

def wiki(self):
    voice("making api call to wiki")

def math(self):
    voice("making api call to wolf frame alpha")

def news(self):
    voice("making api call to top stories from reddit")

def play(self):
    voice(message.replace("play", "playing"))
    song = message.replace("play ", "")
    kit.playonyt(str(song))

def resume(self):
    # use WinRT api in the future
    pyautogui.press('playpause')

def pause(self):
    # use WinRT api in the future
    pyautogui.press('playpause')

def increaseVolume(self):
    pyautogui.press('volumeup')

def decreaseVolume(self):
    pyautogui.press('volumedown')

def mute(self):
    # differentiate between unmute using sound api
    pyautogui.press('volumemute')

def unmute(self):
    # differentiate between mute using sound api
    pyautogui.press('volumemute')

def reset(self):
	pyautogui.hotkey('win', 'x')
	time.sleep(.1)
	pyautogui.press('u')
	time.sleep(.1)
	pyautogui.press('r')

def shutdown(self):
	pyautogui.hotkey('win', 'x')
	time.sleep(.1)
	pyautogui.press('u')
	time.sleep(.1)
	pyautogui.press('u')

def sleep(self):
	pyautogui.hotkey('win', 'x')
	time.sleep(1)
	pyautogui.press('u')
	time.sleep(1)
	pyautogui.press('s')

def minimize(self):
    pyautogui.hotkey('win', 'm')

def maximize(self):
    pyautogui.hotkey('win', 'up')

def restore(self):
    pyautogui.hotkey('win', 'shiftleft', 'm')

def switchApplications(self):
    pyautogui.hotkey('alt', 'tab')

def switchDesktop(self):
    pyautogui.hotkey('win', 'tab')

def openApplication(self):
    voice("opening Application")

def openFile(self):
    voice("opening file")

def date(self):
    t = datetime.datetime.now()
    day = t.strftime("%A")
    date = t.strftime("%d")
    month = t.strftime("%B")
    year = t.strftime("%Y")

    voice('its {}, {} {}, {}'.format(day, month, date, year))

def get_time(self, message):
    t = datetime.datetime.now()
    hour = t.strftime("%H")
    minute = t.strftime("%M")
    ampm = t.strftime("%p")
    hour = int(hour) % 12
    voice('its {} {} {}'.format(hour, minute, ampm))

def day(self):
    voice(self,"it taco tuesday")

def question(self, text:str):
    print('here')
    voice(gpt3_answer(text))