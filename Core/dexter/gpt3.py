import openai

openai.organization = "org-fEhf9cVXO5Gy5N7wHGEu4RjT"
openai.api_key = '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'


def gpt3_answer(question:str, max_tokens=256, model='curie'):
	# required parameters
	examples = [["What is human life expectancy in the United States?","78 years."]]
	examples_context = "In 2017, U.S. life expectancy was 78.6 years."
	documents = ["Puppy A is happy.", "Puppy B is sad."]

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
