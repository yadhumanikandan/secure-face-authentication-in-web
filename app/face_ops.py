import cv2
import os
from os import listdir, curdir
import numpy as np
from os.path import isfile, join


cv2.face.LBPHFaceRecognizer_create() 

face_classifier = cv2.CascadeClassifier('env\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')
# face_classifier = cv2.CascadeClassifier('D:\\Code\\project\\haz\\env\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')

model = cv2.face.LBPHFaceRecognizer_create()


def train_model():
    data_path = 'training_data/'
    onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path,f))]
    Training_Data, Labels = [], []

    for i, files in enumerate(onlyfiles):
        image_path = data_path + onlyfiles[i]
        images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        Training_Data.append(np.asarray(images, dtype=np.uint8))
        Labels.append(i)

    Labels = np.asarray(Labels, dtype=np.int32)
    # model = cv2.face.LBPHFaceRecognizer_create()
    model.train(np.asarray(Training_Data), np.asarray(Labels))
    print("Dataset Model Training Complete!!!!!")


def register_face_extractor_dataset_creation(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)

    if len(faces) == 0:
        return None

    for(x,y,w,h) in faces:
        cropped_face = img[y:y+h, x:x+w]

    return cropped_face


def register_create_dataset_files(unique_name):
    img = cv2.imread('data/received_image.jpg')
    if register_face_extractor_dataset_creation(img) is not None:
        face = cv2.resize(register_face_extractor_dataset_creation(img),(200,200))
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        print(str(unique_name))
        file_name_path = 'training_data/'+str(unique_name)+'.jpg'

        cv2.imwrite(file_name_path,face)
        cv2.putText(face,str(unique_name),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        cv2.imshow('Face Cropper',face)

        return True
    else:
        print("Face not found")
        
        return False


def login_face_detector(img, size = 0.5):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)
    if len(faces) == 0:
        return img,[]

    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,0),2)
        roi = img[y:y+h, x:x+w]
        roi = cv2.resize(roi, (200,200))

    return img,roi


def login_detect_img(img):
    image, face = login_face_detector(img)
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
        else:
            cv2.putText(image, "Unknown", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Face Cropper', image)

    except:
        cv2.putText(image, "Face Not Found", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('Face Cropper', image)
        pass
    
    return False
    