import time
import datetime

# functions for each skill
def weather():
	return 'the weather today is sunny with a high of 69 degrees'

def get_date():
	t = datetime.datetime.now()
	day = t.strftime("%A")
	date = t.strftime("%d")
	month = t.strftime("%B")
	year = t.strftime("%Y")

	return 'its {}, {} {}, {}'.format(day, month, date, year)

def get_time():
	t = datetime.datetime.now()
	hour = t.strftime("%H")
	minute = t.strftime("%M")
	ampm = t.strftime("%p")

	hour = int(hour) % 12

	return 'its {} {} {}'.format(hour, minute, ampm)

def get_day():
	return 'its taco tuesday'


def quit_app():
	quit()

skills_map = {'weather': weather,
		  'time': get_time,
		  'date': get_date,
		  'day': get_day,
		  'quit': quit_app,
		 }