# AgileSoftwareProject
AgileSoftwareProject

## Setup

cd to you working directory

> cd to-your-working-directory

create a virtual environment

> python3 -m env venv

activate the python venv

> source venv/bin/activate

install required python packages

> pip install -r requirements.txt

set up the flask env variables

> export FLASK_APP=flite

> set FLASK_APP=flite

run 

>flask run

## Eample URL:

### Page1:

> http://127.0.0.1:5000/api/direct-destinations?origin=NRT&max=50

### Page2:

> http://127.0.0.1:5000/api/ticket-prices?originalLocation=NRT&destinationLocation=LAX&date=2022-11-01

## Testing
> pytest