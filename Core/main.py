import time
import zmq
import threading
import multiprocessing
import time
from assistant import Dexter
from gesture.hand_detection import HandDetection
import speech_recognition as sr


def zmq_sock():
	context = zmq.Context()
	socket = context.socket(zmq.REP)
	socket.bind("tcp://127.0.0.1:5555")

	while True:

		#  Wait for incoming request from client
		print("Listening...")
		message = socket.recv()
		print("Received request: %s\nSending response" % message)

		#  Do some other stuff
		time.sleep(1)

		#  Send reply back to client
		socket.send_string("What it do")


def launch_dexter():
	dex = Dexter(debug=True)
	dex.listen()


def launch_gesture():
	gest = HandDetection() 
	gest.loop()


def sr_test():

	while True:
		try:
			with sr.Microphone(device_index=0) as mic:
				#self.recognizer.adjust_for_ambient_noise(mic,duration=0.2)
				#audio = self.recognizer.listen(mic)
				#text = self.recognizer.recognize_google(audio)
				#text = text.lower()
				print(f"You said:\n{text}")
				if (text != ""):
					self.message = text
					return text
				else:
					print("empty string")
		except Exception as ex:
			print(ex)


if __name__ == '__main__':
	#Establish a socket to start listening for incoming messages on
	#zmq_sock()

	d = multiprocessing.Process(target=launch_dexter)
	d.start()

	g = multiprocessing.Process(target=launch_gesture)
	g.start()

	
	# for i in reversed(range(100)):
	# 	print('killing application in ' + str(i) + ' seconds')
	# 	time.sleep(1)
	
	# d.terminate()
	# g.terminate()