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

def play():
    song = message.replace("play", "")
    print(song)
    kit.playonyt(str(song))

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
    print("hello")

def goodbye():
    speak("goodbye")

mappings = {
    'greeting' : greeting,
    'goodbye' : goodbye,
    'play' : play
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