import time
import threading
import multiprocessing
import time
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from flask import Flask
from pydantic import BaseModel
from gesture import launch_gesture
from assistant import launch_dexter
import requests
import json
import os
from settings import *
from typing import Optional

app = FastAPI()


settings = load_settings()


dex = None
if settings.dexter_on_startup:
	dex = multiprocessing.Process(target=launch_dexter)
	dex.start()

gest = None
if settings.gesture_on_startup:
	gest = multiprocessing.Process(target=launch_gesture)
	gest.start()



@app.post('/settings/')
async def settings_update(r: GeneralSettings):
	print('settings')
	write_general_settings(r)
	return Response(content=json.dumps({"test":"hi"}))



@app.post('/voice-settings/')
async def voice_settings():
	return ''

@app.post('/gesture-settings/')
async def gesture_settings(r:GestureSettingList):
	print('updating gesture settings')
	write_gesture_settings(r)
	return Response(content=json.dumps({"message":"gesture settings accepted"}))


@app.get('/get-intents/')
async def get_intents():
	print(os.getcwd())
	intent_path = os.path.join(os.getcwd(), 'assistant/model/intents.json')

	if os.path.exists(intent_path):
		f = open(intent_path)
		data = json.load(f)
		print(type(data))
		
		f.close()

		if 'intents' in data:
			return Response(content=json.dumps(data), media_type="application/json")



@app.post('/train-assistant/')
async def train_assistant():
	os.chdir('assistant/model/')
	from trainAssistant import train_assistant
	train_assistant()
	os.chdir('..')
	os.chdir('..')
	return 'level up'


@app.get('/')
async def index():
	return 'Hello World'


@app.post('/dexter-control/')
async def start_stop_dexter(cmd=None):
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
async def start_stop_dexter(cmd=None):
	print(cmd)
	
	global gest
	
	if cmd == 'start':
		
		if gest is None:
			gest = multiprocessing.Process(target=launch_gesture)
			gest.start()
			print('gesture started')
			return 'gesture started'
		else:
			print('gesture already started')
			return 'gesture already started'
	elif cmd == 'stop' and gest is not None:
		gest.terminate()
		gest = None
		print('gesture stopped')
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



