import pyttsx3
import pyaudio
import speech_recognition as sr
from gtts import gTTS
import datetime
import warnings
import wikipedia
from skills import *
import time
from multiprocessing import Process

MIC_SOURCE = 2
WAKE_WORDS = ["Dexter", "hey Dexter", "ok computer", "Okay computer" "hey computer"]

def get_voices():
	voices = engine.getProperty('voices')
	for voice in voices:
		print(voice, voice.id)
		engine.setProperty('voice', voice.id)
		engine.say("Hello World!")
		engine.runAndWait()
		engine.stop()


def listen_for_wake():
	sleep = True

	while sleep:
		with sr.Microphone(MIC_SOURCE) as source:
			print("Waiting for wake word")
			recorded_audio = recognizer.listen(source, timeout=3)
		try:
			
			print("Recognizing")
			start = time.time()
			text = recognizer.recognize_google(
					recorded_audio, 
					language="en-US"
				)
			print("Detection time: {}".format((time.time() - start)))
			print("Decoded Text : {}".format(text))

			for word in WAKE_WORDS:
				if word.lower() in text.lower():
					print("AWOKEN")
					handle_query(text)
					break

		except Exception as ex:
			print(ex)


def recordAudio():
	with sr.Microphone(MIC_SOURCE) as source:
		print("Recording for 4 seconds")
		recorded_audio = recognizer.listen(source, timeout=4)
		print("Done recording")
	try:
		print("Recognizing the text")
		text = recognizer.recognize_google(
				recorded_audio, 
				language="en-US"
			)
		print("Decoded Text : {}".format(text))

	except Exception as ex:
		print(ex)


def speak(text:str):
	engine.say(text)
	engine.runAndWait()


def handle_query(query:str):
	print(query)

	# call function based on query
	keys = skills_map.keys()
	for key in keys:
		if key in query.lower():
			print(key)
			reply = skills_map[key]()
			engine.say(reply)
			engine.runAndWait()


if __name__ == '__main__':
	engine = pyttsx3.init()
	recognizer = sr.Recognizer()

	engine.say("Hey, my name is Dexter. How can I help?")
	engine.runAndWait()

	listen_for_wake()