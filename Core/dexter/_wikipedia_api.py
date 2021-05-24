import wikipedia
from nlp import *

def ask_wikipedia(query:str, num_sentences=2):
	query = parse_query(query)
	
	titles = wikipedia.search(text, results=5)
	print(titles)
	if len(titles) > 0:
		print()
		print()
		query = titles[0]
		print(query)
		print()
		print()
		print('Asking: {}'.format(query))
		try:
			res = wikipedia.summary(query, sentences=num_sentences)
			print(res)
			res = clean_response(res)
			print(res)
			return res
		except Exception:
			res = "I could not find anything on that subject sir"
	else:
		res = "I could not find anything on that subject sir"

	
	return res