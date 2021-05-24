import pyautogui
import time
import re

def open_windows_menu(*args):
	pyautogui.press('win')
	return ''

def open_file_explorer(*args):
	pyautogui.hotkey('win', 'i')
	return ''

def open_settings(*args):
	pyautogui.hotkey('win', 'i')
	return ''

def minimize(*args):
	pyautogui.hotkey('win', 'm')
	return ''

def restore_windows(*args):
	pyautogui.hotkey('win', 'shiftleft', 'm')
	return ''

def task_view(*args):
	pyautogui.hotkey('win', 'tab')
	return ''

def maximize_current_window(*args):
	pyautogui.hotkey('win', 'up')
	return ''

def enter(*args):
	pyautogui.press('enter')
	return ''

def search(*args):
	pyautogui.press('browsersearch')
	return ''

def playpause(*args):
	pyautogui.press('playpause')
	return ''

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
	return ''