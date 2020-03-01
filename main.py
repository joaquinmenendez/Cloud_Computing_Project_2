import pandas as pd
from flask import Flask, render_template, request, flash, redirect
import os
from werkzeug.utils import secure_filename

# initialize variables
app = Flask(__name__)

# I will need to work around this in the future. Setting basic configuration.
app.secret_key = "secret key"
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
    app.run(host='0.0.0.0.', port=8080, debug=True)