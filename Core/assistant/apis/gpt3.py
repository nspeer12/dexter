import openai

openai.organization = "org-fEhf9cVXO5Gy5N7wHGEu4RjT"
openai.api_key = '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'


def gpt3_answer(question:str, max_tokens=256, model='curie'):
	# required parameters
	examples = [["What is human life expectancy in the United States?","78 years."]]
	examples_context = "In 2017, U.S. life expectancy was 78.6 years."
	documents = [""]

	response = openai.Answer.create(model=model, 
									examples_context=examples_context, 
									examples=examples, question=question, 
									documents=documents,
									max_tokens=max_tokens)

	# initialize default answer
	ans = 'I do not have an answer for you sir'

	# clean response
	if 'answers' in response:
		if len(response['answers']) > 0:
			ans = response['answers'][0]

		# they add in new line characters to the response
		ans = ans.split('\n')
		
		if len(ans) > 0:
			ans = ans[0]

	return ans


if __name__ == '__main__':
	print(gpt3_answer('what is the capital of india'))


def gpt3_convo(question:str, context, max_tokens=256, model='curie'):
	
	examples = [["What is human life expectancy in the United States?","78 years."]]
	examples_context = "In 2017, U.S. life expectancy was 78.6 years."
	documents = [""]

	response = openai.Answer.create(model=model, 
									examples_context=examples_context, 
									examples=examples, question=question, 
									documents=[context],
									max_tokens=max_tokens)

	print(response)
	# clean response
	if 'answers' in response:
		if len(response['answers']) > 0:
			ans = response['answers'][0]

		# they add in new line characters to the response
		ans = ans.split('\n')
		
		if len(ans) > 0:
			ans = ans[0]

	return response
	