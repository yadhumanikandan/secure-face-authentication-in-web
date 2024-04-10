from flask import Flask, render_template, request, jsonify, redirect, url_for, session # type: ignore
import cv2
import numpy as np
import base64
import os
from os import listdir, curdir
from os.path import isfile, join
from PIL import Image
from datetime import datetime



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



img = cv2.imread('data/received_image.jpg')



def face_extractor_dataset_creation(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)

    if len(faces) == 0:
        return None

    for(x,y,w,h) in faces:
        cropped_face = img[y:y+h, x:x+w]

    return cropped_face


def create_dataset_files(time):

    
    img = cv2.imread('data/received_image.jpg')

    if face_extractor_dataset_creation(img) is not None:
    # count+=1
        face = cv2.resize(face_extractor_dataset_creation(img),(200,200))
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        # print(str(time))
        # file_name_path = 'D:/DATAS/'+str(count)+'.jpg'
        file_name_path = 'D:/DATAS/'+str(time)+'.jpg'

        cv2.imwrite(file_name_path,face)

        cv2.putText(face,str(time),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        cv2.imshow('Face Cropper',face)
        return True
    else:
        print("Face not found")
        return False

    # if cv2.waitKey(1)==13 or count==100:
    #     break

create_dataset_files('djlfkjslkdj')