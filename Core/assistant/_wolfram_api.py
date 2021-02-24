import wolframalpha 
from nlp import *


def ask_wolfram(question:str):
	print(question)
	# App id obtained by the above steps 
	app_id = 'APER4E-58XJGHAVAK'
	app_id = '5KJ8J9-9P4HUVL3RX'

	# Instance of wolf ram alpha  
	# client class 
	client = wolframalpha.Client(app_id) 
	  
	# Stores the response from  
	# wolf ram alpha 
	res = client.query(question) 
	  
	# Includes only text from the response 
	answer = next(res.results).text 
	  
	print(answer)

	# handle math questions
	# ex: 2 + 2 = 4 -> 'the answer is four'
	if answer.isnumeric():
		answer = 'the answer is ' + answer
		
	return answer

if __name__ == '__main__':
	ask_wolfram('what is 2+2')