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
import csv
import torch
import torch.nn as nn
from model.assistantModel import NeuralNet
import speech_recognition
import nltk
from nltk.stem import WordNetLemmatizer


MIC_SOURCE = 1
WAKE_WORDS = ["Dexter", "hey Dexter", "texture", "computer", "Okay computer" "hey computer", "dex"]

class Dexter:

	def __init__(self):
		self.startup = time.time()

		ASSISTANT_PATH = "model/AssistantModel.pth"
		# read in csv for num features and classes
		with open("model/Assistant_features.csv") as f:
			reader = csv.reader(f)
			Assistant_features = [row[0] for row in reader]
		self.num_features = len(Assistant_features)

		self.feature_dict = {}
		for i in range(self.num_features):
			self.feature_dict[Assistant_features[i]] = i

		with open("model/Assistant_labels.csv") as f:
			reader = csv.reader(f)
			self.Assistant_labels = [row[0] for row in reader]
		self.num_classes = len(self.Assistant_labels)

		self.model = NeuralNet(self.num_features,self.num_classes)
		self.model.load_state_dict(torch.load(ASSISTANT_PATH))
		self.model.eval()
		print("loaded assistant model")

		self.recognizer = speech_recognition.Recognizer()

		self.mappings = {
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
			'time' : get_time,
			'day' : day,
			'question' : question,
		}

	def wake_word(self):
		# loop until wake word is detected
		pass

	def get_input(self):
		# get input from microphone -> google api -> text
		pass

	def process_input(self, message):
		bag = [0] * self.num_features
		words = nltk.word_tokenize(message)
		for word in words:
			if word.lower() in self.feature_dict:
				bag[self.feature_dict[word.lower()]] += 1

		bag = torch.from_numpy(np.array(bag))
		# print(bag)
		output = self.model.forward(bag.float())
		prediction = self.Assistant_labels[torch.argmax(output)]
		print(prediction)

		if prediction in self.mappings.keys():
			self.mappings[prediction](self, message)


	def listen(self):
		
		#playsound('sounds/boing.wav')
		
		run = True


		print('Listening...')


		with sr.Microphone() as source:
			
			while run:

				try:
					#print("Waiting for wake word")

					#recognizer.adjust_for_ambient_noise(source, duration=0.5)
					try:
						recorded_audio = self.recognizer.listen(source, timeout=1)

					except Exception as ex:
						if debug:
							print(ex)

						continue

					print("Recognizing")

					start = time.time()

					text = self.recognizer.recognize_google(
							recorded_audio,
							language='en-US')

					decode_time = time.time() - start

					if debug:
						print("Detection time: {}".format(decode_time))

					with open('logs/decode-time.txt', 'a') as decode:
						decode.write("{}\n".format(decode_time))
						decode.close()


					if debug:
						print("Decoded Text : {}".format(text))

					
					self.process_input(text)

					#handle_query(text)

					with open('logs/total-response-time.txt', 'a') as trt:
						trt.write("{}\n".format(time.time() - start))
						trt.close()


				except Exception as ex:
					print(ex)


if __name__ == '__main__':
	debug = True

	dexter = Dexter()
	dexter.listen()

	
