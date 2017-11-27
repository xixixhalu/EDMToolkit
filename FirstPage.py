import os

import GenerateCode

from flask import flash
from flask import render_template, Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

from Backend.Parser.parse_DM_File import analyzer as p

ana = p()

UPLOAD_FOLDER = 'Input'
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
    filename_str = ""
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
            filename_str = filename.split(".")[0]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    #Parse XML and generate JSON
    ana.DM_File_Analyze('Input', {'DM_Input_type': "Simple_XML"}, filename_str)

    #Parse JSON and generate code
    element_names, server_url = GenerateCode.generate_all(filename_str)

    print element_names
    print server_url

    #Convert collection names to dictionary for ID to name mapping
    dict_mapping = {}
    id = 1

    for element in element_names:
        dict_mapping[id] = [element, element_names[element]]
        id+=1

    print dict_mapping

    #Pass required data to the template
    description_data = {"collection_names":dict_mapping, "db_name":filename_str}
    description_data["server_url"] = server_url

    print description_data

    #Render the template
    return render_template('result_page.html', **description_data)

if __name__ == '__main__':
    app.run()