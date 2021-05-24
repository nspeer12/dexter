from precise_runner import PreciseEngine, PreciseRunner
from playsound import playsound


engine = PreciseEngine('precise-engine/precise-engine', 'computer-en.pb')
runner = PreciseRunner(engine, on_activation=lambda: playsound('boing.wav'))
runner.start()

# Sleep forever
from time import sleep
while True:
    sleep(10)