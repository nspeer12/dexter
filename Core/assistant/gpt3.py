import openai

openai.organization = "org-fEhf9cVXO5Gy5N7wHGEu4RjT"
openai.api_key = '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'

#response = openai.Completion.create(engine="davinci", prompt="This is a test", max_tokens=5)
#print(response)

#print(openai.Engine.list())


def gpt3_answer(question:str, max_tokens=256, model='davinci'):
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