# Cloud_Computing_Project_2
## Docker Container Project

---
### This is a draft!!!

## Create a project
> insert pictures here

## Enable APIs
> insert pictures here


## Create a virtualenv
> virtualenv ./.descrive_csv

## Activate the virtualenv
> source ./.descrive_csv/bin/activate

## Create a bucket for your project.
#### Remove italics for your own variables

> export PROJECT_NAME=*carbon-zone-269620*

> gsutil mb -p $PROJECT_NAME -c standard -l *us-east1* -b on gs://*describe_csv_bucket*/

** Note : If you want to run directly from the Docker file to modify this values in the `Dockerfile` file **

## Create a `requirements.txt`
```bash
flask==1.1.1
pandas
```

## Create a `Makefile`
```bash
install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

all: install
```

## Install all the requirements
> make all


## Write your app `app.py`
```python
import flask
import pandas as pd

#initialize 
app = Flask(__name__)

#read csv
desribe_csv = pd.read_csv(VAR).describe()

print(describe_csv)
```
