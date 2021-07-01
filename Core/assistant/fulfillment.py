import requests
import urllib


def fulfillment_api(query:str, context):
	f = {"query" : query}

	url = "https://dexter.speer.ai/api/?" + urllib.parse.urlencode(f)
	response = requests.get(url)

	if response.status_code == 200:
		response = response.content.decode('UTF-8')
	else:
		response = "I could not handle that response"
		
	return response


if __name__ == '__main__':
	fulfillment_api('hello world!')