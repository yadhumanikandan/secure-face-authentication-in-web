from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import cv2
import numpy as np
import base64
import os
from os import listdir, curdir
from os.path import isfile, join

app = Flask(__name__)
app.secret_key = "lasdfoh389h9qhweohpqe8hgqh9hqwh49hq9hgq9h"

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True


cv2.face.LBPHFaceRecognizer_create() 

data_path = 'D:/DATAS/'
onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path,f))]

Training_Data, Labels = [], []

for i, files in enumerate(onlyfiles):
    image_path = data_path + onlyfiles[i]
    images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    Training_Data.append(np.asarray(images, dtype=np.uint8))
    Labels.append(i)

Labels = np.asarray(Labels, dtype=np.int32)

model = cv2.face.LBPHFaceRecognizer_create()

model.train(np.asarray(Training_Data), np.asarray(Labels))

print("Dataset Model Training Complete!!!!!")


face_classifier = cv2.CascadeClassifier('D:\\Code\\project\\haz\\env\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')

def face_detector(img, size = 0.5):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)

    if len(faces) == 0:
        return img,[]

    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,0),2)
        roi = img[y:y+h, x:x+w]
        roi = cv2.resize(roi, (200,200))

    return img,roi


def detect_img(img):
# while True:
    # ret, frame = cap.read()

    image, face = face_detector(img)
    img_path = os.path.join(curdir, 'received_image.jpg')
    cv2.imwrite(img_path, image)

    try:
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        result = model.predict(face)

        if result[1] < 500:
            confidence = int(100*(1-(result[1])/300))



        if confidence > 82:
            cv2.putText(image, "yadhu", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            cv2.imshow('Face Cropper', image)
            return True
            # return redirect(url_for("home"))

        else:
            cv2.putText(image, "Unknown", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Face Cropper', image)


    except:
        cv2.putText(image, "Face Not Found", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('Face Cropper', image)
        pass
    
    return False
    # if cv2.waitKey(1)==13:
    #     break



@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route('/check-user')
def check_user():
    return render_template('camera.html') ################## change to camera.html

@app.route('/home')
def home():
    if "faceauth" in session and session["faceauth"] == True:
        return render_template("home.html")
    else:
        return redirect(url_for("check_user"))

@app.route('/detect', methods=['POST'])
def detect():
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


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
