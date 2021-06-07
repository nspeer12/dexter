import time
import zmq
import threading
import multiprocessing
from multiprocessing import Pool
import time
import speech_recognition as sr
from fastapi import FastAPI, Request
from flask import Flask
from gesture import launch_gesture
from assistant import launch_dexter

app = FastAPI()

dex = None
gest = None
pool = Pool(2)


def zmq_sock():
	context = zmq.Context()
	socket = context.socket(zmq.REP)
	socket.bind("tcp://127.0.0.1:8888")

	#  Wait for incoming request from client
	print("Listening...")
	message = socket.recv()
	print("Received request: %s\nSending response" % message)


	#  Send reply back to client
	socket.send_string("Socket Connected")

	return socket


@app.get('/')
async def index():
	return 'Hello World'


@app.post('/dexter-control/')
def start_stop_dexter(cmd=None):
	print(cmd)

	if cmd == 'start':
		global dex
		dex = multiprocessing.Process(target=launch_dexter)
		dex.start()
		return 'dexter started'

	elif cmd == 'stop' and dex is not None:
		dex.terminate()
		return 'dexter stopped'

	return 'cmd not recieved'


@app.post('/gesture-control/')
def start_stop_dexter(cmd=None):
	print(cmd)

	if cmd == 'start':
		global gest
		gest = multiprocessing.Process(target=launch_gesture)
		gest.start()
		return 'gesture started'

	elif cmd == 'stop' and dex is not None:
		gest.terminate()
		return 'gesture stopped'

	return 'cmd not recieved'



@app.post('/stop-gesture')
async def stop_gesture():
	'''
	global gest
	if gest is not None:
		
		return 'gesture stopped'
	else:
		'''
	return 'gesture not started'

