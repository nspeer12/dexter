import pyautogui
import time

def open_windows_menu():
	pyautogui.press('win')
	return ''

def open_file_explorer():
	pyautogui.hotkey('win', 'i')
	return ''

def open_settings():
	pyautogui.hotkey('win', 'i')
	return ''

def minimize():
	pyautogui.hotkey('win', 'm')
	return ''

def restore_windows():
	pyautogui.hotkey('win', 'shiftleft', 'm')
	return ''

def task_view():
	pyautogui.hotkey('win', 'tab')
	return ''

def maximize_current_window():
	pyautogui.hotkey('win', 'up')
	return ''

def enter():
	pyautogui.press('enter')
	return ''

def search():
	pyautogui.press('browsersearch')
	return ''

def playpause():
	pyautogui.press('playpause')
	return ''

def sleep():
	pyautogui.hotkey('win', 'x')
	time.sleep(1)
	pyautogui.press('u')
	time.sleep(1)
	pyautogui.press('s')
	return 'good night sir'


def shutdown():
	pyautogui.hotkey('win', 'x')
	time.sleep(1)
	pyautogui.press('u')
	time.sleep(1)
	pyautogui.press('u')
	return 'good night sir'


def reset():
	pyautogui.hotkey('win', 'x')
	time.sleep(1)
	pyautogui.press('u')
	time.sleep(1)
	pyautogui.press('r')
	return 'good night sir'


def hibernate():
	pyautogui.hotkey('win', 'x')
	time.sleep(1)
	pyautogui.press('u')
	time.sleep(1)
	pyautogui.press('h')
	return 'good night sir'