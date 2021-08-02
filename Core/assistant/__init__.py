import os
from os import path
import speech_recognition as sr
import datetime
import time
from multiprocessing import Process
from scipy.io.wavfile import write
from playsound import playsound
import csv
import torch
import torch.nn as nn
import speech_recognition
import nltk
from nltk.stem import WordNetLemmatizer
import wave
import numpy as np
import pvporcupine
import pyaudio
import struct
import pandas as pd

# need to move path back
import sys

from assistant.skills import *
from assistant.utils.intro import intro
from assistant.model.assistantModel import NeuralNet
from assistant.nlp import *
from assistant.fulfillment import fulfillment_api, log_query


class Dexter:

	def __init__(self, debug=False, audio=True, input_device=1):
		self.startup = time.time()
		self.debug = debug
		self.cwd = os.getcwd()

		self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

		# Define CSV paths
		dir_name = path.dirname(__file__)

		path.join(dir_name, 'csv/gesture_label.csv')

		ASSISTANT_PATH = path.join(dir_name, "model/AssistantModel.pth")
		FEATURES_PATH = path.join(dir_name, "model/Assistant_features.csv")
		LABELS_PATH = path.join(dir_name, "model/Assistant_labels.csv")
		INTENT_PATH = path.join(dir_name, "model/intents.json")

		# read in intents.json as a dataframe
		print("loading intents.json")

		with open(INTENT_PATH) as f:
			self.settings_json = json.load(f)["intents"]
			self.df = pd.DataFrame(self.settings_json)

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

		self.model = NeuralNet(self.num_features, self.num_classes)
		self.model.load_state_dict(torch.load(ASSISTANT_PATH, map_location=self.device))
		self.model.eval()
		
		if self.debug:
			print("loaded assistant model")

		

		self.mappings = {
			'Greeting' : greeting,
			'Introduction' : introduction,
			'Goodbye' : goodbye,
			'Wiki' : fulfillment_api,
			'Math' : math,
			'Play' : play,
			'Resume' : resume,
			'Pause' : pause,
			'Increase Volume' : increaseVolume,
			'Decrease Volume' : decreaseVolume,
			'Mute' : mute,
			'Unmute' : unmute,
			'Reset' : reset,
			'Shutdown' : shutdown,
			'Sleep' : sleep,
			'Minimize' : minimize,
			'Maximize' : maximize,
			'Restore' : restore,
			'Switch Applications' : switchApplications,
			'Switch Desktop' : switchDesktop,
			'Date' : date,
			'Time' : get_time,
			'Day' : day,
			'Question' : fulfillment_api,
      		'Weather' : weather,
			'Bitcoin Price' : bitcoin_price,
			'Convo' : fulfillment_api,
			'Print Chat Log' : print_chat_log,
			'Fullscreen' : fullscreen,
			'idk' : idk,
			"Type": type_
		}


		self.record_history = False
		self.context = ""
		self.query_history = []
		self.response_history = []

		if audio:
			self.mic = input_device
			self.audio = None
			self.audio_stream = None

			self.porcupine = pvporcupine.create(keyword_paths=['assistant/porcupine/hey-dexter-windows.ppn'])
			self.mute_on_wake = True
			self.timeout = 5

			self.recognizer = speech_recognition.Recognizer()
			self.recognizer.dynamic_energy_threshold = False
			
			print('adjusting for audio levels')
			with sr.Microphone(device_index=self.mic) as source:
				self.recognizer.adjust_for_ambient_noise(source, duration=5)

			print('done adjusting')
			self.beep_on_listen = True



	def start_audio_stream(self):
		self.audio = pyaudio.PyAudio()

		self.audio_stream = self.audio.open(
								rate=self.porcupine.sample_rate,
								channels=1,
								format=pyaudio.paInt16,
								input=True,
								frames_per_buffer=self.porcupine.frame_length)


	def stop_audio_stream(self):
		self.audio_stream.close()
		self.audio.terminate()


	def hotword(self):
		porcupine = None
		pa = None
		audio_stream = None

		self.start_audio_stream()

		listen = True

		try:
			
			while listen:

				pcm = self.audio_stream.read(self.porcupine.frame_length)
				pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)

				keyword_index = self.porcupine.process(pcm)

				if keyword_index >= 0:
					self.stop_audio_stream()
					print("Hotword Detected")
					self.listen()
					self.start_audio_stream()

		except Exception as ex:
			print(ex)



	def listen(self):

		with sr.Microphone(device_index=self.mic) as source:
		
			try:
				print('Listening...')

				if self.beep_on_listen:
					playsound('assistant/sounds/beep.wav')
				
				recorded_audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)
				
				start = time.time()
				print("Recognizing")
				
				
				if self.beep_on_listen:
					playsound('assistant/sounds/beep-beep.wav')

					
				text = self.recognizer.recognize_google(
						recorded_audio,
						language='en-US')

			except Exception as ex:
				
				if self.beep_on_listen:
					playsound('assistant/sounds/beep-boop.wav')

				if self.debug:
					print(ex)

				return

			else:
				
				decode_time = time.time() - start

				if self.debug:
					print("Detection time: {}".format(decode_time))
										
				detection, res = self.process_input(text)

				if not isinstance(res, type(None)):
					voice(res, quality='high')

				if self.debug:
					print("Total Response Time: {}\n".format(time.time() - start))
				
				#log_query(text, detection, res)
		
		return


	def process_input(self, text):
		text = clean_text(text)

		bag = [0] * self.num_features
		words = nltk.word_tokenize(text)
		for word in words:
			if word.lower() in self.feature_dict:
				bag[self.feature_dict[word.lower()]] += 1

		bag = torch.from_numpy(np.array(bag))
		
		output = self.model.forward(bag.float())
		# print(torch.argmax(output))
		prediction = self.Assistant_labels[torch.argmax(output)]
		record = self.df.loc[(self.df["tag"] == prediction)]

		if (len(record.iloc[0]) > 0):
			if (record.iloc[0]["actionType"] == "default_action"):
				print(record.iloc[0]["default_action_name"])
				res = self.mappings[record.iloc[0]["default_action_name"]](text, self.context)
			elif (record.iloc[0]["actionType"] == "macro"):
				macroString = record.iloc[0]["macro"].split(" + ")
				for string in macroString:
					pyautogui.keyDown(string)
				# temp = macroString[::-1]
				for string in macroString:
					pyautogui.keyUp(string)
				res = "Executing Macro"
			elif (record.iloc[0]["actionType"] == "script"):
				print("script", record.iloc[0]["script"])
				if os.path.exists(record.iloc[0]["script"]):
					exec(open(record.iloc[0]["script"]).read())
					res = "Executing Script"
			elif (record.iloc[0]["actionType"] == "file"):
				print("file", record.iloc[0]["file_path"])
				if os.path.exists(record.iloc[0]["file_path"]):
					os.startfile(record.iloc[0]["file_path"])
					res = "Opening File"
			elif (record.iloc[0]["actionType"] == "application"):
				print("application", record.iloc[0]["application"])
				if os.path.exists(record.iloc[0]["application"]):
					os.startfile(record.iloc[0]["application"])
					res = "Opening Application"
			

			if self.record_history and isinstance(res, str) and isinstance(text, str):


				self.query_history.append(text)

				self.response_history.append(res)

				self.context += 'Human: ' + str(text) + '\n'
				self.context += 'AI: ' + str(res) + '\n'

			return prediction, res

		
			
        
		# # TODO: prediction threshold

		# if prediction in self.mappings.keys():
	
		# 	function_to_run = self.mappings[prediction]

		# 	if self.debug:
		# 		print(prediction)

		# 	res = function_to_run(text, self.context)
			
		# 	# record command and response
		# 	if self.record_history and isinstance(res, str) and isinstance(text, str):


		# 		self.query_history.append(text)

		# 		self.response_history.append(res)

		# 		self.context += 'Human: ' + str(text) + '\n'
		# 		self.context += 'AI: ' + str(res) + '\n'
			
			
		# 	return prediction, res


def launch_dexter(settings):

    dexter = Dexter(debug=settings.debug,
					input_device=settings.input_device)
    dexter.hotword()