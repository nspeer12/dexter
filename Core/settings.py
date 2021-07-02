import os
import json
from pydantic import BaseModel


class GeneralSettings(BaseModel):
	dexter_on_startup: bool
	gesture_on_startup: bool
	output_device: int
	input_device: int


def load_settings():
	if os.path.exists('settings.json'):
		with open('settings.json') as f:
			data = json.load(f)
			return GeneralSettings(data)


def write_general_settings(settings: GeneralSettings):

	data = json.loads(settings.json())

	with open('settings.json', 'w') as f:
		print(data)
		json.dump(data, f, sort_keys=True, indent=4)


if __name__ == '__main__':
	settings = load_settings()