import torch
import torch.nn as nn
from assistantModel import NeuralNet
from assistantDataLoader import assistantDataset
import speech_recognition
import nltk
from nltk.stem import WordNetLemmatizer
import csv
import numpy as np
import pyttsx3 as tts
import sys
import json
import pywhatkit as kit

ASSISTANT_PATH = "AssistantModel.pth"

# read in csv for num features and classes
with open("Assistant_features.csv") as f:
    reader = csv.reader(f)
    Assistant_features = [row[0] for row in reader]
num_features = len(Assistant_features)

feature_dict = {}
for i in range(num_features):
    feature_dict[Assistant_features[i]] = i

with open("Assistant_labels.csv") as f:
    reader = csv.reader(f)
    Assistant_labels = [row[0] for row in reader]
num_classes = len(Assistant_labels)

model = NeuralNet(num_features,num_classes)
model.load_state_dict(torch.load(ASSISTANT_PATH))
model.eval()
print("loaded assistant model")

WAKE_WORDS = ["Dexter", "hey Dexter", "texture", "computer", "Okay computer" "hey computer", "dex"]
recognizer = speech_recognition.Recognizer()
speaker = tts.init()
speaker.setProperty('rate', 150)

def speak(text):
    speaker.say(text)
    speaker.runAndWait()

def wakeWord():
    while True:
        print("waiting for wake word")
        text = getMessage()
        for word in WAKE_WORDS:
                    if word.lower() in text.lower():
                        speak("Yessir, how may I help you?")
                        return True

def getMessage():
    while True:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic,duration=0.2)
                audio = recognizer.listen(mic)

                text = recognizer.recognize_google(audio)
                text = text.lower()

                print(f"Recongized {text}")
                if (text != ""):
                    return text

        except Exception as ex:
            print(ex)

def greeting():
    speak("greeting")

def introduction():
    speak("I am Dexter")

def goodbye():
    speak("goodbye")

def wiki():
    speak("making api call to wiki")

def math():
    speak("making api call to wolf frame alpha")

def news():
    speak("making api call to top stories from reddit")

def play():
    speak(message.replace("play", "playing"))
    song = message.replace("play ", "")
    kit.playonyt(str(song))

def resume():
    # use WinRT api in the future
    pyautogui.press('playpause')

def pause():
    # use WinRT api in the future
    pyautogui.press('playpause')

def increaseVolume():
    pyautogui.press('volumeup')

def decreaseVolume():
    pyautogui.press('volumedown')

def mute():
    # differentiate between unmute using sound api
    pyautogui.press('volumemute')

def unmute():
    # differentiate between mute using sound api
    pyautogui.press('volumemute')

def reset():
	pyautogui.hotkey('win', 'x')
	time.sleep(.1)
	pyautogui.press('u')
	time.sleep(.1)
	pyautogui.press('r')

def shutdown():
	pyautogui.hotkey('win', 'x')
	time.sleep(.1)
	pyautogui.press('u')
	time.sleep(.1)
	pyautogui.press('u')

def sleep():
	pyautogui.hotkey('win', 'x')
	time.sleep(1)
	pyautogui.press('u')
	time.sleep(1)
	pyautogui.press('s')

def minimize():
    pyautogui.hotkey('win', 'm')

def maximize():
    pyautogui.hotkey('win', 'up')

def restore():
    pyautogui.hotkey('win', 'shiftleft', 'm')

def switchApplications():
    pyautogui.hotkey('alt', 'tab')

def switchDesktop():
    pyautogui.hotkey('win', 'tab')

def openApplication():
    speak("opening Application")

def openFile():
    speak("opening file")

def date():
    speak("opening file")
    t = datetime.datetime.now()
    day = t.strftime("%A")
    date = t.strftime("%d")
    month = t.strftime("%B")
    year = t.strftime("%Y")
    speak('its {}, {} {}, {}'.format(day, month, date, year))

def time():
    t = datetime.datetime.now()
    hour = t.strftime("%H")
    minute = t.strftime("%M")
    ampm = t.strftime("%p")
    hour = int(hour) % 12
    speak('its {} {} {}'.format(hour, minute, ampm))

def day():
    speak("it taco tuesday")

mappings = {
    'greeting' : greeting,
    'introduction' : introduction,
    'goodbye' : goodbye,
    'wiki' : wiki,
    'math' : math,
    'news' : news,
    'play' : play,
    'resume' : resume,
    'pause' : pause,
    'increaseVolume' : increaseVolume,
    'decreaseVolume' : decreaseVolume,
    'mute' : mute,
    'unmute' : unmute,
    'reset' : reset,
    'shutdown' : shutdown,
    'sleep' : sleep,
    'minimize' : minimize,
    'maximize' : maximize,
    'restore' : restore,
    'switchApplications' : switchApplications,
    'switchDesktop' : switchDesktop,
    'openApplication' : openApplication,
    'openFile' : openFile,
    'date' : date,
    'time' : time,
    'day' : day,

    }

# while True:
#     if (wakeWord()):
#         message = getMessage()
#         print(message)
#         assistant.request(message)

while True:
    # if (wakeWord()):
        # message = getMessage()
    message = input()
    # print(message)
    bag = [0] * num_features
    words = nltk.word_tokenize(message)
    for word in words:
        if word.lower() in feature_dict:
            bag[feature_dict[word.lower()]] += 1

    bag = torch.from_numpy(np.array(bag))
    print(bag)
    output = model.forward(bag.float())
    prediction = Assistant_labels[torch.argmax(output)]
    print(prediction)

    if prediction in mappings.keys():
        mappings[prediction]()