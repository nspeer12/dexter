import wikipedia

def ask_wikipedia(query:str, num_sentences=2):
	print(query)
	
	titles = wikipedia.search(query, results=5)
	print(titles)
	if len(titles) > 0:
		res = titles[0]
		print(res)
		print('Asking: {}'.format(query))
		try:
			res = wikipedia.summary(query, sentences=num_sentences)
			print(res)
			return res
		except Exception as ex:
			print(ex)
			res = "I could not find anything on that subject sir"
	else:
		res = "I could not find anything on that subject sir"

	
	return res