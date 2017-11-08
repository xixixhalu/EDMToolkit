import os

from flask import flash
from flask import render_template, Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'GeneratedCode'
ALLOWED_EXTENSIONS = set(['xml'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('upload_xml.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    #Parse XML and generate JSON

    #Parse JSON and generate code
        #TODO: Generate DB name and port dynamically
        #TODO: Decide what data is required for the REST API Page

    #Pass required data to the template

    #Render the template
    return render_template('result_page.html')

if __name__ == '__main__':
    app.run()