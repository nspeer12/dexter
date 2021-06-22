from pydantic import BaseModel
import os
import json


class Settings(BaseModel):
	# user preferences
	name: str

	# program settings
	launch_on_startup: bool
	core_host: str
	core_port: int
	dashboard_host: str
	dashboard_port: int

	# voice assistant settings
	voice_on_startup: bool

	# gesture settings
	gesture_on_startup: bool


# idk if this works :/
def load_settings():
	if os.path.exists('settings.json'):
		f = open('settings.json')
		data = json.load(f)
		print(type(data))
		for x in data:
			if type(x) == 'str':
				os.environ[str(x)] = data[str(x)]
				print(str(x))


def write_settings(settings: Settings):
	data = json.loads(settings.json())

	with open('settings.json', 'w') as f:
		json.dump(data, f, sort_keys=True, indent=4)


if __name__ == '__main__':
	load_settings()