import time
import threading
import multiprocessing
import time
from fastapi import FastAPI, Request
from flask import Flask
from gesture import launch_gesture
from assistant import launch_dexter
import requests
import json
import os
from settings import *

app = FastAPI()

dex = None
gest = None
setts = load_settings()
print(setts)

@app.post('/settings')
def settings_update(settings:Settings):
	write_settings(settings)


@app.get('/')
async def index():
	return 'Hello World'


@app.post('/dexter-control/')
def start_stop_dexter(cmd=None):
	print(cmd)

	if cmd == 'start':
		global dex
		dex = multiprocessing.Process(target=launch_dexter, args=(setts,))
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



