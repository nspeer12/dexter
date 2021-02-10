import pyttsx3
import pyaudio
import speech_recognition as sr
from gtts import gTTS
import datetime
import warnings
import wikipedia

MIC_SOURCE = 2

def get_voices():
	voices = engine.getProperty('voices')
	for voice in voices:
		print(voice, voice.id)
		engine.setProperty('voice', voice.id)
		engine.say("Hello World!")
		engine.runAndWait()
		engine.stop()



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


if __name__ == '__main__':
	engine = pyttsx3.init()
	recognizer = sr.Recognizer()

	engine.say("hello world")

	engine.say("My name is Dexter")
	engine.runAndWait()

	recordAudio()