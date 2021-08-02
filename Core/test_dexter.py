from assistant import launch_dexter
from settings import *
from multiprocessing import Process, Array

if __name__ ==  "__main__":
	arr = Array('i', [0,0])
	settings = load_settings()
	launch_dexter(settings, arr=arr)