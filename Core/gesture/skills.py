import pyautogui

pyautogui.PAUSE = 0.01

def leftClick():
    pyautogui.click()

# what about double left click?

def rightClick():
    pyautogui.click(button="right")

def zoomIn():
    pyautogui.hotkey('ctrl', '=')

def zoomOut():
    pyautogui.hotkey('ctrl', '-')

def scrollUp():
    pyautogui.scroll(10)

def scrollDown():
    pyautogui.scroll(-10)

def goBack():
    pyautogui.hotkey("browserback")

def goForward():
    pyautogui.hotkey("browserforward")

def switchApp():
    pyautogui.hotkey('alt', 'tab')

def switchDesktop():
    ppyautogui.hotkey('win', 'tab')

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
    pyautogui.hotkey('win', 'm')

def play():
    pyautogui.press('playpause')

def pause():
    pyautogui.press('playpause')

def nextTrack():
    pyautogui.press('nexttrack')

def prevTrack():
    pyautogui.press('prevtrack')

def increaseVolume():
    pyautogui.press('volumeup')

def decreaseVolume():
    pyautogui.press('volumedown')

def unmute():
    pyautogui.press('volumemute')

def mute():
    pyautogui.press('volumemute')