import requests
import os
from playsound import playsound
import time
import random
import multiprocessing


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

		# get auth
		headers = {
		  'Content-Type': 'application/x-www-form-urlencoded'
		}
		payload = 'client_id=nspeer252@gmail.com&secret=t%G$blDdSgBeD7E0nQeQ'

		r = requests.post('https://api.replicastudios.com/auth', headers=headers, data=payload)

		token = r.json()['access_token']


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
		
		if 'url' in res:
			url = res['url']
		else:
			print('Replica Error')
			print(res)
			return 0


		# download file
		cwd = os.getcwd()

		# use random file name
		filename = "tmp.wav"

		output_path = filename
		data = requests.get(url).content

		
		with open(output_path, "wb") as f:
			f.write(data)
			f.close()


		'''
		with open('logs/replcia-time.txt', 'a') as f:
			f.write("{}\n".format(time.time() - start))
			f.close()
		'''

	except():
		voice(text)


	if debug:
		print('Response took:{}', time.time() - start)

	playsound(output_path)

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

