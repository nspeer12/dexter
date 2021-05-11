import speech_recognition as sr
import datetime
from skills import *
import time
from multiprocessing import Process
from voice import *
from _wikipedia_api import *
from _wolfram_api import *
from nlp import *
import sounddevice as sd
from scipy.io.wavfile import write
from nlp import *
from intro import intro
from gpt3 import *


MIC_SOURCE = 1
WAKE_WORDS = ["Dexter", "hey Dexter", "texture", "computer", "Okay computer" "hey computer", "dex"]




def get_voices():
	voices = engine.getProperty('voices')
	for voice in voices:
		print(voice, voice.id)
		engine.setProperty('voice', voice.id)
		engine.say("Hello World!")
		engine.runAndWait()
		engine.stop()


def listen_for_wake():
	wait = True

	with sr.Microphone() as source:
		recognizer.adjust_for_ambient_noise(source, duration=2)
		
		while wait:
			try:
				print("Waiting for wake word")
				recorded_audio = recognizer.listen(source, timeout=1)
				print("Recognizing")
				start = time.time()

				text = recognizer.recognize_google(
						recorded_audio,
						language='en-US'
					)
				print("Detection time: {}".format((time.time() - start)))
				print("Decoded Text : {}".format(text))
			except Exception as ex:
				print(ex)
				continue

			for word in WAKE_WORDS:
				if word.lower() in text.lower():
					handle_query(text)
					break


def record_audio():
	with sr.Microphone(MIC_SOURCE) as source:
		print("Recording for 4 seconds")
		recorded_audio = recognizer.listen(source, timeout=4)
		print(recorded_audio)
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
	recognizer = sr.Recognizer()
	intro()
	#voice("Hello sir, my name is Dexter, you're virtual assistant. How can I help you.")
	listen_for_wake()

	
	#listen_for_wake()

	
