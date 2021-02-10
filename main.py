import pyttsx3
import pyaudio
import speech_recognition as sr
from gtts import gTTS
import datetime
import warnings
import wikipedia

MIC_SOURCE = 2
WAKE_WORD = "Dexter"

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
			print("Adjusting noise ")
			recognizer.adjust_for_ambient_noise(source, duration=1)
			print("Waiting for wake word")
			recorded_audio = recognizer.listen(source)
			print("Done recording")
		try:
			print("Recognizing the text")
			text = recognizer.recognize_google(
					recorded_audio, 
					language="en-US"
				)
			print("Decoded Text : {}".format(text))

			if WAKE_WORD in text:
				print("AWOKEN")
				speak("how can I help you")
				sleep = False

		except Exception as ex:
			print(ex)

def recordAudio():
	with sr.Microphone(MIC_SOURCE) as source:
		print("Adjusting noise ")
		recognizer.adjust_for_ambient_noise(source, duration=1)
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


if __name__ == '__main__':
	engine = pyttsx3.init()
	recognizer = sr.Recognizer()

	engine.say("hello world")

	engine.say("My name is Dexter")
	engine.runAndWait()

	listen_for_wake()