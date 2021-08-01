from assistant import launch_dexter
from settings import *

if __name__ ==  "__main__":
	settings = load_settings()
	launch_dexter(settings)