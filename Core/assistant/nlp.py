import spacy
from string import punctuation
import re

# download with python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")

def parse_query(query:str):
	# extract meaning from a query
	
	# example query:
	# 'Who was Leonardo da Vinci'
	# should return
	# 'leonardo da vinci'
	
	
	doc = nlp(clean_query(query))

	result = []
	pos_tag = ['PROPN', 'NOUN', 'ADJ']

	nouns = [chunk.text for chunk in doc.noun_chunks]

	for chunk in doc.noun_chunks:
		final_chunk = ""
		for token in chunk:
			if (token.pos_ in pos_tag):
				final_chunk =  final_chunk + token.text + " "
		if final_chunk:
			result.append(final_chunk.strip())


	for token in doc:
		if (token.text in nlp.Defaults.stop_words or token.text in punctuation):
			continue
		if (token.pos_ in pos_tag):
			result.append(token.text)

	res = list(set(result))

	# take max len object from extracted text
	# ex: ['new', 'york', 'city', 'new york city'] -> 'new york city'
	max_res = ''

	for r in res:
		if len(r) > len(max_res):
			max_res = r

	return max_res


def clean_text(query:str):
	query = query.replace('hey dexter', '')
	query = query.replace('hey Dexter', '')
	query = query.replace('Dexter', '')
	query = query.replace('dexter', '')
	query = query.replace('texture', '')
	return query.lower()