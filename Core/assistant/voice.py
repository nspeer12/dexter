import requests
import os
from playsound import playsound
import time
import random
import multiprocessing
import simpleaudio as sa

# get auth
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
payload = 'client_id=nspeer252@gmail.com&secret=t%G$blDdSgBeD7E0nQeQ'
r = requests.post('https://api.replicastudios.com/auth', headers=headers, data=payload)
token = r.json()['access_token']


def get_voices():
	root_url = 'https://api.replicastudios.com'

	# get auth
	headers = {
	  'Content-Type': 'application/x-www-form-urlencoded'
	}
	payload = 'client_id=nspeer252@gmail.com&secret=t%G$blDdSgBeD7E0nQeQ'

	r = requests.post('https://api.replicastudios.com/auth', headers=headers, data=payload)

	token = r.json()['access_token']
	url = f"{root_url}/voice"
	response = requests.request("GET", url, headers={'Authorization': f'Bearer {token}'}, data={})
	voices = response.json()
	print(f'Found {len(voices)} voices.')

	for voice in voices:
		print(voice)

	return voices


def voice_replica(text:str, debug=False):
	start = time.time()

	try:
		# get voice
		headers = {
		  'Authorization': 'Bearer {}'.format(token)
		}
		
		# transform to ssml and (optionally, change pitch)
		text = '<speak><prosody pitch="0%" rate="medium" volume="soft">' + text + '</prosody></speak>'

		r = requests.get('https://api.replicastudios.com/speech', params={
		  'txt': text,  'speaker_id': '53be3ead-fb29-457f-b67c-aad9e9fb28f1', 'quality': 'low'
		}, headers = headers)

		res = r.json()

		if 'sample_rate' in res:
			sample_rate = res['sample_rate']

		if 'url' in res:
			url = res['url']
		else:
			print('Replica Error')
			print(res)
			return 0

		data = requests.get(url).content

		sa.play_buffer(data, 1, 2, sample_rate)


	except():
		voice(text)


	if debug:
		print('Response took:{}', time.time() - start)


def voice_engine(text:str):
	engine = pyttsx3.init()
	engine.say(text)
	engine.runAndWait()


def voice(text, quality='high'):
	if quality == 'high':
		voice_replica(text)
	else:
		voice_engine(text)


if __name__=="__main__":
	get_voices()
	#voice("Hello Sir, my name is Dexter. How can I help you today")

