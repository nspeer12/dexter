import wolframalpha 
# from nlp import *
import inflect

def ask_wolfram(question:str):
	print(question)
	# App id obtained by the above steps 
	#app_id = 'APER4E-58XJGHAVAK'
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
	#infl = inflect.engine()
	#answer = infl.number_to_words(answer)
	#print(answer
	
	answer = re.sub("/", " divided by ", answer)
	answer = re.sub("(irreducible)", "", answer)
	answer = re.sub("sqrt", "times the square root of", answer)
	answer = re.sub(r'\)', "", answer)
	answer = re.sub(r'\(', "", answer)
	answer = 'the answer is ' + answer
	print(answer)

	return answer

if __name__ == '__main__':
	ask_wolfram('what is 2+2')