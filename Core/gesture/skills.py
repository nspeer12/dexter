import pyautogui
import random


pyautogui.PAUSE = 0.01

def leftClick():
    pyautogui.click()

def doubleClick():
    pyautogui.click(clicks=2)

# what about double left click?

def rightClick():
    pyautogui.click(button="right")

def zoomIn():
    pyautogui.hotkey('ctrl', '=')

def zoomOut():
    pyautogui.hotkey('ctrl', '-')

def scrollUp():
    pyautogui.scroll(1000)

def scrollDown():
    pyautogui.scroll(-1000)

def goBack():
    pyautogui.hotkey("browserback")

def goForward():
    pyautogui.hotkey("browserforward")

def switchApp():
    pyautogui.hotkey('alt', 'tab')

def switchDesktop():
    pyautogui.hotkey('win', 'tab')

def slideAppLeft():
    pyautogui.hotkey('win', 'up')
    pyautogui.hotkey('win', 'up')
    pyautogui.hotkey('win', 'left')
    pyautogui.hotkey('esc')

def slideAppRight():
    pyautogui.hotkey('win', 'up')
    pyautogui.hotkey('win', 'up')
    pyautogui.hotkey('win', 'right')
    pyautogui.hotkey('esc')

def maximizeApp():
    pyautogui.hotkey('win', 'up')

def minimizeApp():
    # pyautogui.hotkey(f'win', 'm') # all applications
    pyautogui.hotkey('win', 'down') # one application

def play():
    pyautogui.press('playpause')

def pause():
    pyautogui.press('playpause')

def nextTrack():
    pyautogui.press('nexttrack')

def prevTrack():
    pyautogui.press('prevtrack')

def increaseVolume():
    print("up")
    pyautogui.press('volumeup', presses=5)

def decreaseVolume():
    print("down")
    pyautogui.press('volumedown', presses=5)

def unmute():
    pyautogui.press('volumemute')

def mute():
    pyautogui.press('volumemute')

def windowLeft():
    pyautogui.hotkey('win', 'shift', 'left')


def windowRight():
    pyautogui.hotkey('win', 'shift', 'rightf')

def closeWindow():
    pyautogui.hotkey('alt', 'f4')


def fullscreen():
    pyautogui.press('f11')
    pyautogui.press('f')


