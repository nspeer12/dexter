import requests
import os
from playsound import playsound
import time

# get auth
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}
payload = 'client_id=nspeer252@gmail.com&secret=t%G$blDdSgBeD7E0nQeQ'

r = requests.post('https://api.replicastudios.com/auth', headers = headers, data = payload)

token = r.json()['access_token']


# get voice
headers = {
  'Authorization': 'Bearer ' + token
}

def voice(text:str):
	start = time.time()
	r = requests.get('https://api.replicastudios.com/speech', params={
	  'txt': text,  'speaker_id': 'c4fe46c4-79c0-403e-9318-ffe7bd4247dd'
	}, headers = headers)

	res = r.json()

	url = res['url']

	print(url)

	# download file
	cwd = os.getcwd()
	output_path = os.path.join(cwd, "tmp.wav")
	print(output_path)
	data = requests.get(url).content

	with open(output_path, "wb") as f:
		f.write(data)
		f.close()

	print(time.time() - start)
	playsound("tmp.wav")
