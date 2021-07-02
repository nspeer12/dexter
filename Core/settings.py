import os
import json


class Settings():
	def __init__(self, dictionary):
		for k, v in dictionary.items():
			setattr(self, k, v)
			print(k,v)

def load_settings():
	if os.path.exists('settings.json'):
		with open('settings.json') as f:
			data = json.load(f)
			return Settings(data)


def write_settings(settings: Settings):
	# might not be working
	data = json.loads(settings)

	with open('settings.json', 'w') as f:
		json.dump(data, f, sort_keys=True, indent=4)


if __name__ == '__main__':
	settings = load_settings()