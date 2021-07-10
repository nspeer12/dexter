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
	camera_index: int


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
						camera_index=data['camera_index'])

			return settings


def write_general_settings(settings: GeneralSettings):

	data = json.loads(settings.json())

	with open('settings.json', 'w') as f:
		json.dump(data, f, sort_keys=True, indent=4)
		f.close()

def write_gesture_settings(settings: GestureSettingList):
	data = json.loads(settings.json())

	with open('gesture/csv/gestureSettings.json', 'w') as f:
		json.dump(data['settings'], f, sort_keys=True, indent=4)
		f.close()

if __name__ == '__main__':
	settings = load_settings()