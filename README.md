# Docker containerization
## Project 2

This is a tutorial of how to use Docker containerization. You can see a quick demostration [here.](https://youtu.be/0v3HIwOZ064)

**Previous projects**<br>
- [Continuous Delivery of Flask Application on GCP](https://github.com/joaquinmenendez/Cloud_Computing_Project_1)<br>
**Next projects**<br>
- [Using Google Cloud Functions to develop a Serverless Data Engineering Pipeline](https://github.com/joaquinmenendez/Cloud_Computing_Project_4)
-  [Submitting a Pyspark job to a Spark cluster on GCP](https://github.com/joaquinmenendez/Cloud_Computing_Project_3)<br>


The README file contains all the instructions to build a Flask app from scratch, build a docker image to run it everywhere and deploy this image as an app using Cloud Run Services (GCS).
You can have access to a cloud version of this app runing on GCS [here](https://describer-ions6p5noa-ue.a.run.app).

> *This is a beta version, do not upload files larger than 50 MB*

The same app could be deploy using APP Engine from GCS. To see an example of how to do this check my other [repository](https://github.com/joaquinmenendez/Cloud_Computing_Project_1)


## Create a project
![create_project](https://user-images.githubusercontent.com/43391630/75630460-f32acd00-5bb8-11ea-8a74-4484a66f9223.png)

## Create a bucket for your project [optional]
#### Rename with your own variables
```bash
export PROJECT_NAME=carbon-zone-269620

gsutil mb -p $PROJECT_NAME -c standard -l us-east1 -b on gs://describe_csv_bucket/
```
*Note : This is not necessary. The app works using a `temp` folder inside the container.
 Only need to do this is you are going to deploy this app on App Engine. The docker has a limited amount of space to upload files*

## Create a `requirements.txt`
```bash
flask==1.1.1
pandas
werkzeug
```

## Create a `Makefile`
```bash
install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

all: install
```

## Create a virtualenv
```
virtualenv ./.descrive_csv
# Activate the virtualenv
source ./.descrive_csv/bin/activate
# Install all the requirements
make all
```

## Write your Docker file
```bash
#From Image selected
FROM python:3.7.3-stretch

# Working Directory

WORKDIR /describer

# Copy source code to working directory

COPY . main.py /describer/

# Install packages from requirements.txt

RUN pip install --upgrade pip &&\

    pip install -r requirements.txt

#Espose a port

EXPOSE 8080

CMD ["python", "main.py"]
```

## Write your app `main.py`
*Caveat! you need to have a `main.py` script in order to deploy an app. If not GSC cannot interact with your app.*

```python
import pandas as pd
from flask import Flask, render_template, request, flash, redirect
import os
from werkzeug.utils import secure_filename

#Initialize variables
app = Flask(__name__)

#I need to work around this
app.secret_key = "secret key" #Flask ask me for a key. 
app.config['UPLOAD_FOLDER'] = './temp'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 #50 mb 
ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/iris')
def describe_iris():
    iris = pd.read_csv('./data/iris.csv').describe()
    iris_html = iris.to_html(header="true", table_id="table")
    return '''
    <title>Describer APP</title>
    <p><b>Welcome to Describer ©</b></p>
    <p>This APP allows you to upload any .csv file and see a quick summary of the data inside.</p>
    <table> <tr>Iris dataset</tr>
    {}</table></br>
    <a href="./upload" target="_top"> <strong>Upload your own dataset!</strong></a>
    '''.format(iris_html)

@app.route('/')
def hello():
    return f'<title>Describer APP</title>\
    <p><b>Welcome to Describer ©</b></p>\
    <p>This APP allows you to upload any .csv file and see a quick summary of the data inside.</p>\
    See an example with the classic  <a href="{"./iris"}">Iris dataset.</a> </br>\
    Because classics never go out of style</br>\
    <p> Or <a href="./upload" target="_top"> \
            <strong>Upload your own dataset!</strong></a></p>'


@app.route('/upload')
def upload_form():
	return render_template('upload.html')
@app.route('/upload', methods=['POST'])
def upload_file():
	global filename #maybe there is a better way than using global, but it's the easier way now
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename) 
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('File successfully uploaded')
			return redirect('/describe')
		else:
			flash('Allowed file types are csv')
			return redirect(request.url)

@app.route('/describe')
def describe_data():
    desc_file = pd.read_csv('./temp/' + filename).describe()
    desc_file_html = desc_file.to_html(header="true", table_id="table")
    return '''
    <title>Describer APP</title>
    <p><b>Welcome to Describer ©</b></p>
    <p>This APP allows you to upload any .csv file and see a quick summary of the data inside.</p>
    <p> You uploaded the file <strong>{}</strong> </p>
    <table><tr>This is the summary of the data</tr>
    {}</table></br>
    <a href="./upload" target="_top"> <strong>Continue exploring!</strong></a>
    '''.format(filename, desc_file_html )

# Useful also to visualize locally
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
```
## Build and deploy your image to Docker Hub
```bash
#Select the name of your image
docker build --tag=describer .

# Set a dockerpath with user and name of the image
dockerpath="mellijoaco/describer"

# Authenticate & Tag
echo "Docker ID and Image: $dockerpath"
docker login && docker image tag describer $dockerpath

# Push Image
docker image push $dockerpath 

#To run the container. You would need to expose a port to connect with the docker port.
#In this case I am using 8080 for both.
docker run -p 8080:8080 -it mellijoaco/describer bash   

#run the flask app
python3 main.py
```

## GCR
You can also create an Image and upload this one to the Google Clour Repository (GCR). 
You can deploy this image using the Cloud Run Services and it will be executed as a docker container in a VM.
To do this you will need to have an `app.py` file. 

You would need to enable certaing options.

![enable_options](https://user-images.githubusercontent.com/43391630/75631313-b1e9eb80-5bbf-11ea-849d-bac67488b5be.png)

```bash
#This would take some time
#gcloud run deploy --image gcr.io/PROJECT_ID/name 
gcloud builds submit --tag gcr.io/carbon-zone-269620/describer
# Deploy the project
gcloud run deploy --image gcr.io/carbon-zone-269620/describer --platform managed
```
You can have access to the cloud version [here](https://describer-ions6p5noa-ue.a.run.app)
