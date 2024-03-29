import time
from threading import *
import multiprocessing
from multiprocessing import Process, Array
import time
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from gesture import HandDetection, launch_gesture
from assistant import Dexter, launch_dexter
import requests
import json
import os
from settings import *
from typing import Optional
import uvicorn
import sys
import os


from fastapi.middleware.cors import CORSMiddleware




print("running main.py")
print(os.getcwd())
os.chdir('../Core')
print(os.getcwd())

app = FastAPI()

origins = [
	"http://localhost",
	"http://localhost:3000",
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.get('/status/')
async def status():
	dex_status = "offline"
	gest_status = "offline"
	if (gesArr[0] == 0):
		gest_status = "offline"
	elif (gesArr[0] == 1):
		gest_status = "starting"
	elif (gesArr[0] == 2):
		gest_status = "online"

	if (dexArr[0] == 0):
		dex_status = "offline"
	elif (dexArr[0] == 1):
		dex_status = "starting"
	elif (dexArr[0] == 2):
		dex_status = "online"

	# if dexp != None:
	# 	dex_status = "online"
	
	# if gestp != None:
	# 	gest_status = "online"
	
	return Response(content=json.dumps({"core": "online", "dexter": dex_status, "gesture": gest_status}))

@app.get('/get-settings/')
async def get_settings():
	# print(os.getcwd())
	intent_path = os.path.join(os.getcwd(), 'settings.json')

	if os.path.exists(intent_path):
		f = open(intent_path)
		data = json.load(f)
		# print(data)
		
		f.close()
		res = jsonable_encoder(json.dumps(data))
		return JSONResponse(content=res, media_type="application/json")

@app.post('/update-settings/')
async def settings_update(r: GeneralSettings):
	print('settings')
	write_general_settings(r)
	return Response(content=json.dumps({"message":"user settings accepted"}))


@app.post('/gesture-settings/')
async def gesture_settings(r:GestureSettingList):
	print('updating gesture settings')
	write_gesture_settings(r)
	gesArr[1] = 1
	return Response(content=json.dumps({"message":"gesture settings accepted"}))


@app.get('/get-gestures/')
async def get_gestures():
	# print(os.getcwd())
	gesture_path = os.path.join(os.getcwd(), 'gesture/csv/gestureSettings.json')

	if os.path.exists(gesture_path):
		f = open(gesture_path)
		data = json.load(f)
		# print(data)
		
		f.close()
		res = jsonable_encoder(json.dumps(data))
		return JSONResponse(content=res, media_type="application/json")

@app.post('/intent-settings/')
async def intnet_settings(r: IntentList):
	print('updating intent settings')
	write_intent_settings(r)
	# stop dexter
	# train dexter
	# restart dexter
	return Response(content=json.dumps({"message":"intent settings accepted"}))


@app.get('/get-intents/')
async def get_intents():
	intent_path = os.path.join(os.getcwd(), 'assistant/model/intents.json')

	if os.path.exists(intent_path):
		f = open(intent_path)
		data = json.load(f)
		# print(data)
		f.close()
		res = jsonable_encoder(json.dumps(data))
		return Response(content=json.dumps(res), media_type="application/json")



@app.post('/train-assistant/')
async def train_assistant():
	# TODO: fix this
	print("training Assistant")
	sys.path.append('assistant/model')
	from assistant.model.trainAssistant import train_assistant
	os.chdir('./assistant/model')
	train_assistant()
	os.chdir('..')
	os.chdir('..')
	return 'level up'


@app.get('/')
async def index():
	return 'Hello World'


@app.post('/dexter-control/')
async def start_stop_dexter(cmd=None):
	# print(cmd)

	if cmd == 'start':
		global dexp
		if not dexp:
			dexp = multiprocessing.Process(target=launch_dexter, args=(settings,dexArr))
			dexp.start()
			dexArr[0] = 1
			print("dexter started")
			return 'dexter started'
		else:
			print("dexter already started")
			return 'dexter already started'

	elif cmd == 'stop':
		if dexp:
			dexp.terminate()
			dexp = None
			dexArr[0] = 0
			print('dexter stopped')
			return 'dexter stopped'
		else:
			print('dexter already stopped')
			return 'dexter already stopped'


@app.post('/gesture-control/')
async def start_stop_dexter(cmd=None):
	print(cmd)
	
	global gestp

	if cmd == 'start':
		
		if gestp is None:
			gestp = multiprocessing.Process(target=launch_gesture, args=(settings,gesArr))
			gestp.start()
			gesArr[0] = 1
			print('gesture started')
			return 'gesture started'
		else:
			print('gesture already started')
			return 'gesture already started'

	elif cmd == 'stop':
		if gestp is not None:
			gestp.terminate()
			gestp = None
			gesArr[0] = 0
			print('gesture stopped')
			return 'gesture stopped'
		else:
			print('gesture not started')
			return 'gesture started'

	return 'cmd not recieved'


dex_api= Dexter(audio=False)

@app.get('/api/')
async def local_api(query:str):
	
	try:

		if query:
			print(query)
			res = dex_api.process_input(query)
			print(res)

			response = jsonable_encoder(json.dumps({"data":res}))
			return JSONResponse(content=response, media_type="application/json")
		else:
			return '400'
	except Exception as ex:
		return ex

if __name__ == "__main__":
	settings = load_settings()
	global gesArr
	global dexArr
	gesArr = Array('i', [0,0])
	dexArr = Array('i', [0,0])

	# gesture process
	gestp = None
	if settings.gesture_on_startup:
		gestp = multiprocessing.Process(target=launch_gesture, args=(settings, gesArr))
		gestp.start()
		gesArr[0] = 1

	#dexter process
	dexp = None
	if settings.dexter_on_startup:
		dexp = multiprocessing.Process(target=launch_dexter, args=(settings,dexArr))
		dexp.start()
		dexArr[0] = 1
		
	uvicorn.run(app, host="127.0.0.1", port=8000)