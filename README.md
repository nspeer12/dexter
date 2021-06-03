# Dexter


## Installation

#### Installing Core packages

`cd Core`

set up virtual environment and install requirements

`python3 -m venv env`

on Linux/Mac run `source env/bin/activate`

or on Windows run `env\Scripts\activate.bat`

Now, install the requirements

`pip install -r requirements.txt`

Two additional downloads are needed

`python3 -m spacy download en_core_web_sm`

`python -m nltk.downloader 'punkt'`


#### Installing Dashboard packages

`cd Dashboard`

`npm i -g .`

## Running Applications

#### Running Core

`cd Core`

`python main.py`

to launch individual components, run either `python test_dexter.py` or `python test_gesture.py`

#### Running Dashboard

`cd Dashboard`

`npm start`
