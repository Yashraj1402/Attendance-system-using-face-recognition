import cv2
import numpy as np
import face_recognition
import os
import sys
from datetime import datetime

folderName = input()
path = folderName
image = []
name = []
try:
    myList = os.listdir(path)
except:
    sys.exit('Invalid file name')
# print(myList)
for it in myList:
    curImage = cv2.imread(f'{path}/{it}')
    image.append(curImage)
    name.append(os.path.splitext(it)[0])


def Encodings(images):
    list_of_encodings = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        list_of_encodings.append(encode)
    return list_of_encodings


def markAttendance(personName):
    with open('Attendance.csv', 'r+') as f:
        myData = f.readlines()
        nameList = []
        for line in myData:
            entry = line.split(',')
            nameList.append(entry[0])
        if personName not in nameList:
            now = datetime.now()
            timeLine = now.strftime('%H:%M:%S')
            f.writelines(f'\n{personName},{timeLine}')


encodeKnown = Encodings(image)
# print('Encoding Complete')

# enable web cam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facelocCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, facelocCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame, facelocCurFrame):
        matches = face_recognition.compare_faces(encodeKnown, encodeFace)
        faceDistance = face_recognition.face_distance(encodeKnown, encodeFace)
        # print(faceDistance)
        matchIndex = np.argmin(faceDistance)

        if matches[matchIndex]:
            personName = name[matchIndex].upper()
            # print(personName)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, personName, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(personName)

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)

