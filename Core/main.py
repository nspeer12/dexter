import time
import zmq
import threading
import multiprocessing
from multiprocessing import Pool
import time
import speech_recognition as sr
from fastapi import FastAPI, Request
from gesture import launch_gesture
from assistant import launch_dexter

app = FastAPI()

dex = None
gest = multiprocessing.Process(target=launch_gesture)
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


@app.post('/start-dexter')
async def start_dexter(request:Request):
	global dex
	dex = multiprocessing.Process(target=launch_dexter)
	dex.start()
	return 'dexter started'


@app.post('/stop-dexter')
async def stop_dexter(request:Request):
	global dex
	if dex is not None:
		dex.terminate()
		return 'dexter stopped'
	else:
		return 'dexter not started'

@app.post('/start-gesture')
async def start_gesture():
	global gest
	gest.start()
	return 'gesture started'


@app.post('/stop-gesture')
async def stop_gesture():
	global gest
	if gest is not None:
		gest.terminate()
		return 'gesture stopped'
	else:
		return 'gesture not started'


if __name__ == '__main__':
	
	app.start()
