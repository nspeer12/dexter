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
from precise_runner import PreciseEngine, PreciseRunner
from playsound import playsound


MIC_SOURCE = 1
WAKE_WORDS = ["Dexter", "hey Dexter", "texture", "computer", "Okay computer" "hey computer", "dex"]



recognizer = sr.Recognizer()


class Dexter:

	def __init__(self):
		self.startup = time.time()
		
		


def boing():
	playsound('sounds/boing.wav')


def listen():
	
	playsound('sounds/boing.wav')

	with sr.Microphone() as source:
			
		try:
			#print("Waiting for wake word")

			#recognizer.adjust_for_ambient_noise(source, duration=0.5)
			recorded_audio = recognizer.listen(source, timeout=0.5)
			
			print("Recognizing")
			start = time.time()

			text = recognizer.recognize_google(
					recorded_audio,
					language='en-US')

			decode_time = time.time() - start
			print("Detection time: {}".format(decode_time))

			with open('logs/decode-time.txt', 'a') as decode:
				decode.write("{}\n".format(decode_time))
				decode.close()

			print("Decoded Text : {}".format(text))

			handle_query(text)

			with open('logs/total-response-time.txt', 'a') as trt:
				trt.write("{}\n".format(time.time() - start))
				trt.close()

			return

		except Exception as ex:
			print(ex)

		'''
		for word in WAKE_WORDS:
			if word.lower() in text.lower():
				handle_query(text)

				with open('logs/total-response-time.txt', 'a') as trt:
					trt.write("{}\n".format(time.time() - start))
					trt.close()
		'''


if __name__ == '__main__':
	dex = Dexter()

	engine = PreciseEngine('hotword/precise-engine/precise-engine', 'hotword/computer-en.pb')
	runner = PreciseRunner(engine, on_activation=listen)
	runner.start()

	while True:
		time.sleep(2)

	#intro()
	#voice("Hello sir, my name is Dexter, you're virtual assistant. How can I help you.")
	
	#listen_for_wake()


	
