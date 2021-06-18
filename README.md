# Dexter


## Installation

#### Installing Core packages

`cd Core`

set up virtual environment and install requirements

`python3 -m venv env`

on Linux/Mac run `source env/bin/activate`

or on Windows run `env\Scripts\activate.bat`

-Make sure pip is up to date via `python -m pip install --upgrade pip`

Now, install the requirements

`pip install -r requirements.txt`

Two additional downloads are needed

`python3 -m spacy download en_core_web_sm`

`python -m nltk.downloader 'punkt'`

...If using a mac, pyaudio may not install correctly without portaudio.
To install portaudio, first install homebrew with `ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)`
This may require your password twice.
after that, use `run brew install portaudio`


#### Installing Dashboard packages

`cd Dashboard`

`npm i -g .`

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
