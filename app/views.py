from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify  # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash  # type: ignore
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

        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                session['username'] = username
                # flash("Logged in!", category="success")
                return redirect(url_for("views.cam_login"))
            else:
                flash("password incorrect", category="danger")
                return redirect(url_for("views.login"))
        else:
            flash("user don\'t exists", category="danger")
            return redirect(url_for("views.login"))
    else:
        if "faceauth" in session and session["faceauth"] == True:
            return redirect(url_for('views.home'))
        else:
            return render_template("login.html")
    

@views.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user_exist = User.query.filter_by(username=username).first()

        if user_exist:
            flash("Username already in use!!", category="danger")
            return redirect(url_for("views.signup"))
        elif password1 != password2:
            flash("Password don\'t match", category="danger")
            return redirect(url_for("views.signup"))
        else:
            # try:
            new_user = User(email=email, username=username, password=generate_password_hash(password1)) 
            db.session.add(new_user)
            db.session.commit()

            session['username'] = username

            flash("user created", category="success")
            return redirect(url_for("views.cam_register"))
            # except:
            #     flash("something went wrong! please try again.", category="danger")
            #     return redirect(url_for("auth.signup"))
    else:
        return render_template("signup.html")


@views.route('/cam-login')
def cam_login():
    return render_template('cam_data_login.html')

@views.route('/home')
def home():
    if "faceauth" in session and session["faceauth"] == True:
        return render_template("home.html", username = session["username"])
    else:
        return redirect(url_for("views.login"))
    

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
    
    # train_model()

    img_data = request.form['image']
    img_bytes = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_bytes, np.uint8) 
 
    # Decode image
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    detected = detect_img(image)

    if detected == True:
        session['faceauth'] = True
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        flash('Logged in successfully', category="success")
        # return redirect(url_for('views.home'))
        return jsonify({'result': 'success'})
    elif detected == False:
        return jsonify({'result': 'failure'})
    else:
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------")
        return jsonify({'result': 'failure'})


@views.route('/registertologin')
def register_to_login():
    train_model()
    flash('Face registerd succesfully!! Now you can login to your account', category="success")
    return redirect(url_for('views.login'))


@views.route('/loginunsuccess')
def login_unsuccess():
    flash('Face not detected!!!', category="danger")
    return redirect(url_for('views.login'))


@views.route("/logout")
def logout():
    session.clear()
    flash('You have been logged out!!!', category="danger")
    return redirect(url_for("views.login"))
