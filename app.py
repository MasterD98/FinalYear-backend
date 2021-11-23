from flask import Flask,request,flash,redirect,url_for
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from werkzeug.wrappers import response
UPLOAD_FOLDER = './uploadedImages'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION_TYPE']='filesystem'
app.config['SECRET_KEY'] = "manul"
app.config['SESSION_PERMANENT']= False
if not (os.path.exists(UPLOAD_FOLDER)):
    os.mkdir(UPLOAD_FOLDER)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload_file",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No image part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return ''
    return ''

