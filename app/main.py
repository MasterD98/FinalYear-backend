from flask import Flask,request,flash,redirect
from flask_cors import CORS
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
from PIL import Image 
import numpy as np


app = Flask(__name__)
CORS(app)

dfmodel = load_model('app/Models/dfmodel.tflearn')
akiecmodel = load_model('app/Models/akiecmodel.tflearn')
bklmodel = load_model('app/Models/bklmodel.tflearn')
melmodel = load_model('app/Models/melmodel.tflearn')
nvmodel = load_model('app/Models/nvmodel.tflearn')
vascmodel = load_model('app/Models/vascmodel.tflearn')
skinDiseasesName=["Actinic Keratoses","Benign Keratosis","Dermatofibroma","Vascular Skin Lesion","Melanoma","Melanocytic Nevi","Basal cell carcinoma"]

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

        load_img_rz = Image.open(file).resize((224,224))
        img_array = keras.preprocessing.image.img_to_array(load_img_rz)
        img_array = tf.expand_dims(img_array, 0)  # Create batch axis
        Predictions=[]
        Predictions.append(akiecmodel.predict(img_array)[0][1])
        Predictions.append(bklmodel.predict(img_array)[0][1])
        Predictions.append(dfmodel.predict(img_array)[0][1])
        Predictions.append(vascmodel.predict(img_array)[0][1])
        Predictions.append(melmodel.predict(img_array)[0][1])
        Predictions.append(nvmodel.predict(img_array)[0][1])
        Predictions.append(1-Predictions[np.argmin(Predictions)])
        print(str(Predictions))
        print("Prediction : "+skinDiseasesName[np.argmax(Predictions)])
        return skinDiseasesName[np.argmax(Predictions)]
    return ''
