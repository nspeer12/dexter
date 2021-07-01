import pyautogui
import time
import re

def open_windows_menu(*args):
	pyautogui.press('win')
	return None

def open_file_explorer(*args):
	pyautogui.hotkey('win', 'i')
	return None

def open_settings(*args):
	pyautogui.hotkey('win', 'i')
	return None

def minimize(*args):
	pyautogui.hotkey('win', 'm')
	return None

def restore_windows(*args):
	pyautogui.hotkey('win', 'shiftleft', 'm')
	return None

def fullscreen(*args):
	pyautogui.press('f')
	return None


def task_view(*args):
	pyautogui.hotkey('win', 'tab')
	return None

def maximize_current_window(*args):
	pyautogui.hotkey('win', 'up')
	return None

def enter(*args):
	pyautogui.press('enter')
	return None

def search(*args):
	pyautogui.press('browsersearch')
	return None

def playpause(*args):
	pyautogui.press('playpause')
	return None

def sleep(*args):
	pyautogui.hotkey('win', 'x')
	time.sleep(1)
	pyautogui.press('u')
	time.sleep(1)
	pyautogui.press('s')
	return 'good night sir'


def shutdown(*args):
	pyautogui.hotkey('win', 'x')
	time.sleep(.1)
	pyautogui.press('u')
	time.sleep(.1)
	pyautogui.press('u')
	return 'good night sir'


def reset(*args):
	pyautogui.hotkey('win', 'x')
	time.sleep(.1)
	pyautogui.press('u')
	time.sleep(.1)
	pyautogui.press('r')
	return 'good night sir'


def hibernate(*args):
	pyautogui.hotkey('win', 'x')
	time.sleep(.1)
	pyautogui.press('u')
	time.sleep(.1)
	pyautogui.press('h')
	return 'good night sir'



def type_mode(*args):

	if len(args) > 0:
		text = args[0]
	
	punctuation = {"exclamation point": "!",
					"period": ".",
					"question mark": "?",
					"type": "",
					"comma": ",",
					"enter": "\n",
					}

	for p in punctuation.keys():
		text = re.sub(p, punctuation[p], text)
		print(text)

	print("")
	pyautogui.write(text)

	return ""

def newline(*args):
	pyautogui.press("return")
	return None