# Dexter


## Installation

#### Installing Core packages

`cd Core`

set up virtual environment and install requirements

`python3 -m venv env`

on Linux/Mac run `source env/bin/activate`

or on Windows run `env\Scripts\activate.bat`

-Make sure pip is up to date via `python -m pip install --upgrade pip`

On windows, a manual download of PyAudio may be required. To do this, go to https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
and download the version that corresponds to your version of Python.
(Example: Python 3.9 64-bit is equivalent to PyAudi-0.2.11-cp39-cp39-win_amd64.whl)
Once downloaded, open the command line at the .whl file's directory and type:
`pip install _______.whl`

(...If using a mac, pyaudio may not install correctly without portaudio.)
(To install portaudio on mac, first install homebrew with `ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)`)
(This may require your password twice.)
(after that, use `run brew install portaudio`)

pip install pywin32

Now, install the rest of the requirements

`pip install -r requirements.txt`

Two additional downloads are needed

`python3 -m spacy download en_core_web_sm`

<!---`python -m nltk.downloader 'punkt'`
###This install doesn't work, but the program still runs. Is it necessary? -->


#### Installing Dashboard packages

`cd Dashboard`

<!--`npm i -g .`!-->

## Running Applications

#### Running Core

`cd Core`

`python main.py`

to launch individual components, run either `python test_dexter.py` or `python test_gesture.py`

#### Running Dashboard


Install nodejs at https://nodejs.org/en/download/
check if it is installed with 
`node -v`
and
`npm -v`

`cd Dashboard`

`npm install`

`npm start`
