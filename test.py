from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")
names_path = os.path.join(data_dir, 'names.pkl')
faces_path = os.path.join(data_dir, 'faces_data.pkl')

# Build the absolute path to the cascade file
cascade_path = os.path.join(data_dir, "haarcascade_frontalface_default.xml")

attendance_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Attendance")
if not os.path.exists(attendance_dir):
    os.makedirs(attendance_dir)


from win32com.client import Dispatch

def speak(str1):
    speak = Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)


video=cv2.VideoCapture(0)
facedetect=cv2.CascadeClassifier(cascade_path)

with open(names_path, 'rb') as w:
    LABELS=pickle.load(w)
with open(faces_path, 'rb') as f:
    FACES=pickle.load(f)


knn=KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

COL_NAMES = ["NAME","TIME"]


# Initialize attendance data
attendance = None

marked_attendance = set()  # Keeps track of names that have already been saved

print("📸 Starting attendance system. Press 'O' to save attendance, 'Q' to quit.")

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img)

        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")

        # Draw rectangles and put text
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
        cv2.putText(frame, str(output[0]), (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

        # Set attendance data
        attendance = [str(output[0]), str(timestamp)]
        print(f"👤 Detected: {attendance[0]} at {attendance[1]}")

    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)

    if k == ord("o") or k == ord("O"):
        if attendance is None:
            print("⚠️ No attendance data to save! Make sure a face is detected before pressing 'O'.")
        else:
            name_to_save = attendance[0]
            if name_to_save in marked_attendance:
                print(f"⚠️ Attendance for {name_to_save} has already been recorded.")
                speak(f"Attendance for {name_to_save} is already taken.")
            else:
                speak("Attendance Taken.")
                time.sleep(1)
                csv_file_path = os.path.join(attendance_dir, f"Attendance_{date}.csv")

                if not os.path.isfile(csv_file_path):
                    with open(csv_file_path, "w", newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(COL_NAMES)
                        writer.writerow(attendance)
                    print(f"✅ Attendance saved to new file: {csv_file_path}")
                else:
                    with open(csv_file_path, "a", newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(attendance)
                    print(f"✅ Attendance appended to: {csv_file_path}")

                # Mark this person as attended
                marked_attendance.add(name_to_save)

    if k == ord('q') or k == ord('Q'):
        print("👋 Exiting attendance system.")
        break

video.release()
cv2.destroyAllWindows()

