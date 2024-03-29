import os
import json
from pydantic import BaseModel
from typing import List

class GeneralSettings(BaseModel):
	debug: bool 
	dexter_on_startup: bool
	gesture_on_startup: bool
	output_device: int
	input_device: int
	camera_device: int
	name: str


class GestureSetting(BaseModel):
	starting_position: str
	ending_position: str
	motion: str
	name: str
	action: str
	default_action_name: str
	macro: str
	path: str


class GestureSettingList(BaseModel):
	settings: List[GestureSetting]


class Intent(BaseModel):
	tag: str
	patterns: List[str]
	customizable: bool
	actionType: str
	default_action_name: str
	macro: str
	script: str
	file_path: str
	application: str

class IntentList(BaseModel):
	intents: List[Intent]


def load_settings():
	if os.path.exists('settings.json'):
		with open('settings.json') as f:
			data = json.load(f)
			print(data)
			settings = GeneralSettings(
						debug=data['debug'],
						dexter_on_startup=data['dexter_on_startup'],
						gesture_on_startup=data['gesture_on_startup'],
						output_device=data['output_device'],
						input_device=data['input_device'],
						camera_device=data['camera_device'],
						name=data['name'])

			return settings


def write_general_settings(settings: GeneralSettings):

	data = json.loads(settings.json())

	with open('settings.json', 'w') as f:
		json.dump(data, f, sort_keys=False, indent=4)
		f.close()

def write_gesture_settings(settings: GestureSettingList):
	data = json.loads(settings.json())

	with open('gesture/csv/gestureSettings.json', 'w') as f:
		json.dump(data, f, sort_keys=False, indent=4)
		f.close()

def write_intent_settings(intents: IntentList):
	data = json.loads(intents.json())

	with open('assistant/model/intents.json', 'w') as f:
		json.dump(data, f, sort_keys=False, indent=4)
		f.close()

	# train the model


# def write_intents(intents: IntentList):
# 	data = json.loads(intents.json())

# 	with open('assistant/model/intents-tmp.json', 'w') as f:
# 		json.dump(data[intents], f, sort_keys=True, indent=4)
# 		f.close()


if __name__ == '__main__':
	settings = load_settings()