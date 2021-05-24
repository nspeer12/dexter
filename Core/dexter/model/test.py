from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys
import json
import nltk
from nltk.stem import WordNetLemmatizer

WAKE_WORDS = ["Dexter", "hey Dexter", "texture", "computer", "Okay computer" "hey computer", "dex"]
recognizer = speech_recognition.Recognizer()
speaker = tts.init()
speaker.setProperty('rate', 150)

jsonfile = open('intents.json','r')
jsondata = jsonfile.read()
intents = json.loads(jsondata)
# num_classes = len(jsondata["intents"])
# response_dict = {}
# for i in range(num_classes):
#     response_dict[jsondata["intents"][i]["tag"]] = jsondata["intents"][i]["responses"]

# print(response_dict["greeting"])
lemmatizer = WordNetLemmatizer()
words = []
classes = []
documents = []
ignore_letters = ['!', '?', ',', '.']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word = nltk.word_tokenize(pattern)
        words.extend(word)
        documents.append((word, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_letters]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

training = []

# output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    word_patterns = doc[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    # output_row = list(output_empty)
    # output_row[classes.index(doc[1])] = 1
    output_row = classes.index(doc[1])
    training.append([bag, output_row])

print("words")
print(words)
print("classes")
print(classes)
print("documents")
print(documents)

# def speak(text):
#     speaker.say(text)
#     speaker.runAndWait()

# def wakeWord():
#     while True:
#         print("waiting for wake word")
#         text = getMessage()
#         for word in WAKE_WORDS:
#                     if word.lower() in text.lower():
#                         speak("Yessir, how may I help you?")
#                         return True

# def getMessage():
#     while True:
#         try:
#             with speech_recognition.Microphone() as mic:
#                 recognizer.adjust_for_ambient_noise(mic,duration=0.5)
#                 audio = recognizer.listen(mic)

#                 text = recognizer.recognize_google(audio)
#                 text = text.lower()

#                 print(f"Recongized {text}")
#                 if (text != ""):
#                     return text

#         except Exception as ex:
#             print(ex)


# def greeting():

#     speak("greeting")

# def goodbye():
#     speak("goodbye")

# mappings = {
#     'greeting' : greeting,
#     'goodbye' : goodbye
#     }

# assistant = GenericAssistant('intents.json', intent_methods=mappings)
# # assistant.train_model()
# # assistant.save_model()
# assistant.load_model()
# while True:
#     if (wakeWord()):
#         message = getMessage()
#         print(message)
#         assistant.request(message)