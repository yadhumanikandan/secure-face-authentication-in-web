from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from .models import User
import cv2
import numpy as np
import base64
import os
from os import curdir
import uuid
from .face_ops import detect_img, create_dataset_files, train_model


views = Blueprint("views", __name__)


@views.route("/")
def index():
    return redirect(url_for("views.login"))

@views.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(username)
        return "logged in"
    else:
        if "faceauth" in session and session["faceauth"] == True:
            return render_template("home.html")
        else:
            return render_template("login.html")
    

@views.route("/signup")
def signup():
    return render_template("signup.html")


@views.route('/cam-login')
def cam_login():
    return render_template('cam_data_login.html')

@views.route('/home')
def home():
    if "faceauth" in session and session["faceauth"] == True:
        return render_template("home.html")
    else:
        return redirect(url_for("views.cam_login"))
    

@views.route("/cam-register")
def cam_register():
    return render_template("cam_data_register.html")
    

@views.route("/create_dataset", methods=['POST'])
def create_dataset():
    img_data = request.form['image']
    img_bytes = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_bytes, np.uint8) 
 
    # Decode image
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # current_time = datetime.now()
    # current_time_str = current_time.strftime('%Y-%m-%d_%H:%M:%S')

    # image = face_extractor_dataset_creation(image)
    # image, face = face_detector(image)
    # image = face_extractor_dataset_creation(image)
    img_path = os.path.join(curdir, 'data/received_image.jpg')
    cv2.imwrite(img_path, image)

    unique_string = str(uuid.uuid4())
    # print(unique_string)
    bool1 = create_dataset_files(unique_string)

    # bool1 = create_dataset_files(current_time_str)
    # bool1 = True

    if bool1:
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'failure'})



@views.route('/detect', methods=['POST'])
def detect():
    
    train_model()

    img_data = request.form['image']
    img_bytes = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_bytes, np.uint8) 
 
    # Decode image
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    detected = detect_img(image)

    if detected==True:
        session['faceauth'] = True
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        return jsonify({'result': 'success'})
        # return redirect(url_for("home"))
    if detected==False:
        session["faceauth"] = False
        print("---------------------------------------------------------------------------------------------------------")
        return jsonify({'result': 'failure'})


@views.route('/registertologin')
def register_to_login():
    flash('Face registerd succesfully!! Now you can login to your account', category="success")
    return redirect(url_for('views.login'))


@views.route("/logout")
def logout():
    session.clear()
    flash('You have been logged out!!!', category="danger")
    return redirect(url_for("views.login"))
