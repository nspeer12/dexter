import requests
import os
from playsound import playsound
import time
import random
import pyttsx3

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


def voice_replica(text:str):
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
	
		r = requests.get('https://api.replicastudios.com/speech', params={
		  'txt': text,  'speaker_id': '53be3ead-fb29-457f-b67c-aad9e9fb28f1'
		}, headers = headers)

		res = r.json()
		
		url = res['url']


		# download file
		cwd = os.getcwd()

		# use random file name
		filename = "tmp/tmp{}.wav".format(random.randint(0,10000))

		output_path = os.path.join(cwd, filename)
		print(output_path)
		data = requests.get(url).content

		
		with open(output_path, "wb") as f:
			f.write(data)
		
		f.close()

	except():
		voice(text)


	print('Response took:{}').format(time.time() - start)

	playsound(output_path)

def voice(text:str):
	engine = pyttsx3.init()
	engine.say(text)
	engine.runAndWait()

if __name__=="__main__":
	get_voices()
	#voice("Hello Sir, my name is Dexter. How can I help you today")

