import pyautogui


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

