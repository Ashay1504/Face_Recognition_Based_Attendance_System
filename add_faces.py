import cv2
import pickle
import numpy as np
import os
video=cv2.VideoCapture(0)
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")
cascade_path = os.path.join(data_dir, "haarcascade_frontalface_default.xml")
facedetect = cv2.CascadeClassifier(cascade_path)

# Define absolute paths for the pickle files
names_path = os.path.join(data_dir, 'names.pkl')
faces_path = os.path.join(data_dir, 'faces_data.pkl')

faces_data=[]

i=0

import os

name = os.getenv("USER_NAME")

if not name:
    name = input("Enter Your Name: ")


while True:
    ret,frame=video.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=facedetect.detectMultiScale(gray, 1.3 ,5)
    for (x,y,w,h) in faces:
        crop_img=frame[y:y+h, x:x+w, :]
        resized_img=cv2.resize(crop_img, (50,50))
        if len(faces_data)<=100 and i%10==0:
            faces_data.append(resized_img)
        i=i+1
        cv2.putText(frame, str(len(faces_data)), (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (50,50,255), 1)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (50,50,255), 1)
    cv2.imshow("Frame",frame)
    k=cv2.waitKey(1)
    if k==ord('q') or len(faces_data)==100:
        break
video.release()
cv2.destroyAllWindows()

faces_data=np.asarray(faces_data)
faces_data=faces_data.reshape(100, -1)


if not os.path.exists(names_path):
    names=[name]*100
    with open(names_path, 'wb') as f:
        pickle.dump(names, f)
else:
    with open(names_path, 'rb') as f:
        names=pickle.load(f)
    names=names+[name]*100
    with open(names_path, 'wb') as f:
        pickle.dump(names, f)

if not os.path.exists(faces_path):
    with open(faces_path, 'wb') as f:
        pickle.dump(faces_data, f)
else:
    with open(faces_path, 'rb') as f:
        faces = pickle.load(f)
    faces = np.append(faces, faces_data, axis=0)
    with open(faces_path, 'wb') as f:
        pickle.dump(faces, f)