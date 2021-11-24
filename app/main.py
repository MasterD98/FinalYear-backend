from flask import Flask,request,flash,redirect
from flask_cors import CORS
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
from PIL import Image 

app = Flask(__name__)
CORS(app)

model = load_model('app\Models\dfmodel.tflearn')


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
        predictions = model.predict(img_array)
        score = predictions[0]
        return str(score[1])
    return ''

