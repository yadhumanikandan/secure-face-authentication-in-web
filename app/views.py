from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify  # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash  # type: ignore
import cv2
import numpy as np
import base64
import os
from os import curdir
import uuid
import random
from .face_ops import login_detect_img, register_create_dataset_files, train_model
from . import db 
from .models import User
from .qr import generate_qrcode_png
from .send_mail import send_mail
from .get_ip import get_ip_address


SERVER_ADDRESS = f"{get_ip_address()}:5000"


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
            new_user = User(email=email, username=username, password=generate_password_hash(password1)) 
            db.session.add(new_user)
            db.session.commit()

            session['username'] = username

            flash("user created", category="success")
            return redirect(url_for("views.cam_register"))

    else:
        return render_template("signup.html")


@views.route('/cam-login')  # Route to login using face
def cam_login():
    if "username" in session:
        return render_template('cam_data_login.html')
    else:
        return redirect(url_for('views.login'))


@views.route('/detect', methods=['POST'])  # Route to detect face while logging in
def detect():
    img_data = request.form['image']
    img_bytes = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_bytes, np.uint8) 
 
    # Decode image
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    detected = login_detect_img(image)

    if detected == True:
        session['faceauth'] = True
        print("Face detected")
        flash('Logged in successfully', category="success")
        return jsonify({'result': 'success'})
    elif detected == False:
        return jsonify({'result': 'failure'})
    else:
        return jsonify({'result': 'failure'})


@views.route('/home')
def home():
    if "faceauth" in session and session["faceauth"] == True:
        return render_template("home.html", username = session["username"])
    else:
        flash('Login to enter', category="danger")
        return redirect(url_for("views.login"))
    

@views.route("/cam-register")  # Route to register face
def cam_register():
    if "username" in session:
        return render_template("cam_data_register.html")
    else:
        return redirect(url_for("views.login"))
    

@views.route("/create_dataset", methods=['POST'])  # Route to create dataset when registering
def create_dataset():
    img_data = request.form['image']
    img_bytes = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_bytes, np.uint8) 
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img_path = os.path.join(curdir, 'data/received_image.jpg')
    cv2.imwrite(img_path, image)

    unique_string = str(uuid.uuid4())

    bool1 = register_create_dataset_files(unique_string)

    if bool1:
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'failure'})
    

@views.route("/try-again")
def try_again():
    return render_template("try_again.html")


@views.route("/show-qr")
def show_qr():
    if 'username' in session and "faceauth" not in session:
        user = User.query.filter_by(username=session["username"]).first()
        unique_code = str(uuid.uuid4())
        user.code = unique_code
        db.session.add(user)
        db.session.commit()
        url = f"http://{SERVER_ADDRESS}/reregister-face/{session["username"]}"
        generate_qrcode_png(url, unique_code)
        return redirect(url_for("views.show_qr_code", user_code = unique_code))
        # return redirect(url_for("views.reregister", username_for_otp=session["username"]))


@views.route("/reregister-face/<username_for_otp>", methods=['GET', 'POST'])
def reregister(username_for_otp):
    if request.method == 'POST':
        if "faceauth" not in session:
            username = request.form.get("username")
            password = request.form.get('password')
            otp = request.form.get("otp")

            user = User.query.filter_by(username=username).first()

            otp_stored = user.otp

            print(f"{otp_stored} - {otp}")

            if user:
                if check_password_hash(user.password, password) and otp == otp_stored:
                    session["username"] = username
                    session["reregister"] = "ready"
                    return redirect(url_for("views.faceid_re_register"))
                else:
                    flash("password or otp incorrect", category="danger")
                    return redirect(url_for("views.reregister"))
            else:
                flash("username don\'t exists", category="danger")
                return redirect(url_for("views.reregister"))
        else:
            return redirect(url_for("views.login"))
    else:
        otp_gen = random.randint(1000, 9999)
        user_for_otp = User.query.filter_by(username=username_for_otp).first()
        user_for_otp.otp = otp_gen
        db.session.add(user_for_otp)
        db.session.commit()
        send_mail(user_for_otp.email, otp_gen)

        if "faceauth" not in session:
            return render_template("reregister_password_prompt.html")
        else:
            flash('Login to enter', category="danger")
            return redirect(url_for("views.login"))


@views.route("/faceid-re-register")
def faceid_re_register():
    if ("username" in session and "reregister" in session) and session["reregister"] == "ready":
        session.pop("reregister", None)
        return render_template("cam_data_register.html")
    else:
        return redirect(url_for("views.login"))

@views.route("/<user_code>")
def show_qr_code(user_code):
    if "username" in session and "faceauth" not in session:
        qr_path = f"qr/{user_code}.png"
        return render_template("show_qr.html", qr_path = qr_path)
    else:
        return redirect(url_for("views.login"))


@views.route('/registertologin')  # Route to go from register to login on successfull registration of face
def register_to_login():
    train_model()
    flash('Face registerd succesfully!! Now you can login to your account', category="success")
    return redirect(url_for('views.login'))


@views.route('/loginunsuccess')  # Route to go to try_again page on unsuccesfull face detection
def login_unsuccess():
    flash('Face not detected!!!', category="danger")
    return redirect(url_for('views.try_again'))


@views.route("/logout")
def logout():
    session.clear()
    flash('You have been logged out!!!', category="danger")
    return redirect(url_for("views.login"))
