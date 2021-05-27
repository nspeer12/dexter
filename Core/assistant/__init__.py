from dexter.skills import *
from dexter.utils.intro import intro
from dexter.nlp import *
from dexter.apis.gpt3 import *
from dexter.voice import *
from dexter.apis.wikipedia_api import *
from dexter.apis.wolfram_api import *
from dexter.model.assistantModel import NeuralNet

import os
import speech_recognition as sr
import datetime
import time
from multiprocessing import Process
import sounddevice as sd
from scipy.io.wavfile import write
from precise_runner import PreciseEngine, PreciseRunner
from playsound import playsound
import csv
import torch
import torch.nn as nn
import speech_recognition
import nltk
from nltk.stem import WordNetLemmatizer
import wave
import numpy as np


MIC_SOURCE = 1
WAKE_WORDS = ["Dexter", "hey Dexter", "texture", "computer", "Okay computer" "hey computer", "dex"]



class Dexter:

	def __init__(self, debug=False):
		self.startup = time.time()
		self.debug = debug
		self.cwd = os.getcwd()

		ASSISTANT_PATH = os.path.join(self.cwd, "dexter/model/AssistantModel.pth")
		FEATURES_PATH = os.path.join(self.cwd, "dexter/model/Assistant_features.csv")
		LABELS_PATH = os.path.join(self.cwd, "dexter/model/Assistant_labels.csv")

		# read in csv for num features and classes
		with open(FEATURES_PATH) as f:
			reader = csv.reader(f)
			Assistant_features = [row[0] for row in reader]

		self.num_features = len(Assistant_features)

		self.feature_dict = {}
		for i in range(self.num_features):
			self.feature_dict[Assistant_features[i]] = i

		with open(LABELS_PATH) as f:
			reader = csv.reader(f)
			self.Assistant_labels = [row[0] for row in reader]
		
		self.num_classes = len(self.Assistant_labels)

		self.model = NeuralNet(self.num_features,self.num_classes)
		self.model.load_state_dict(torch.load(ASSISTANT_PATH))
		self.model.eval()
		
		if self.debug:
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

		self.context = ''

	def hotword(self):
		# loop until wake word is detected
		pass

	def get_input(self):
		# get input from microphone -> google api -> text
		while True:
			try:
				with speech_recognition.Microphone() as mic:
					self.recognizer.adjust_for_ambient_noise(mic,duration=0.2)
					audio = self.recognizer.listen(mic)
					text = self.recognizer.recognize_google(audio)
					text = text.lower()
					print(f"You said:\n{text}")
					if (text != ""):
						self.message = text
						return text
					else:
						print("empty string")
			except Exception as ex:
				print(ex)

	def process_input(self, text):
		text = clean_text(text)

		bag = [0] * self.num_features
		words = nltk.word_tokenize(text)
		for word in words:
			if word.lower() in self.feature_dict:
				bag[self.feature_dict[word.lower()]] += 1

		bag = torch.from_numpy(np.array(bag))
		# print(bag)
		output = self.model.forward(bag.float())

		prediction = self.Assistant_labels[torch.argmax(output)]
	
		# TODO: prediction threshold

		if prediction in self.mappings.keys():
			self.mappings[prediction](text, self.context)


	def listen(self):
		
		#playsound('sounds/boing.wav')
		
		run = True


		print('Listening...')


		with sr.Microphone(device_index=1) as source:
			
			#self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
			
			while run:
		
				try:
					recorded_audio = self.recognizer.listen(source, timeout=0.5)
					
					print("Recognizing")

					start = time.time()

					text = self.recognizer.recognize_google(
							recorded_audio,
							language='en-US')

				except Exception as ex:
					if self.debug:
						print(ex)

				else:
					
					decode_time = time.time() - start

					if self.debug:
						print("Detection time: {}".format(decode_time))

					'''
					with open('logs/decode-time.txt', 'a') as decode:
						decode.write("{}\n".format(decode_time))
						decode.close()
					'''

					if self.debug:
						print("Decoded Text : {}".format(text))

											
					self.process_input(text)

					#handle_query(text)

					'''
					with open('logs/total-response-time.txt', 'a') as trt:
						trt.write("{}\n".format(time.time() - start))
						trt.close()
					'''

	def listen_houndify(self):
			
			client_id = 'mLj9gDELeOre8qQtF8nFgg=='
			client_key = 'VSZ20NQYzk1ncWF2DQK3sYKAoCty5fmZcl7vyQIvYJ1eyIGAxOTuGQ9lD6LY5ayhWSowLSyF47Da-4JeQl21IA=='


			#playsound('sounds/boing.wav')
			
			run = True

			print('Listening...')


			with sr.Microphone() as source:
				
				#self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
				
				while run:
			
					try:
						recorded_audio = self.recognizer.listen(source, timeout=0.5)
						
						print("Recognizing")

						start = time.time()

						text = self.recognizer.recognize_houndify(recorded_audio, client_id, client_key)

					except Exception as ex:
						if self.debug:
							print(ex)

					else:
						
						decode_time = time.time() - start

						if self.debug:
							print("Detection time: {}".format(decode_time))

						'''
						with open('logs/decode-time.txt', 'a') as decode:
							decode.write("{}\n".format(decode_time))
							decode.close()
						'''

						if self.debug:
							print("Decoded Text : {}".format(text))

												
						self.process_input(text)

						#handle_query(text)

						'''
						with open('logs/total-response-time.txt', 'a') as trt:
							trt.write("{}\n".format(time.time() - start))
							trt.close()
						'''