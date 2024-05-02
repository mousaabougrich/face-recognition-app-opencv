import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QWidget, QTextEdit
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
import cv2
import mysql.connector
from datetime import datetime


class FaceRecognitionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self.faceDet = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('recognizer/trainingData.yml')

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.face_times = {}  # Store first detection time of each face

    def initUI(self):
        self.setWindowTitle("Face Recognition System")
        self.setGeometry(100, 100, 1200, 720)  

        
        layout = QHBoxLayout()

        # Text Area for User Info
        self.userInfo = QTextEdit()
        self.userInfo.setReadOnly(True)
        self.userInfo.setFixedWidth(200)  # Adjust width as necessary

        # Label for displaying the camera feed
        self.imageLabel = QLabel(self)
        self.imageLabel.setFixedSize(960, 720)  # Larger and fixed size for video feed

        layout.addWidget(self.userInfo)
        layout.addWidget(self.imageLabel)

        # Central Widget
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def update_frame(self):
        ret, img = self.cam.read()
        if ret:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.faceDet.detectMultiScale(gray, 1.3, 5)
            info_text = ""  # To collect text information about all detected faces
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                ID, conf = self.recognizer.predict(gray[y:y+h, x:x+w])

                threshold = 60  # Confidence threshold
                if conf < threshold:
                    if ID not in self.face_times:
                        self.face_times[ID] = datetime.now().strftime("%H:%M:%S")  # Record first detection time
                    profile = self.getprofile(ID)
                    if profile:
                        text = f"Detected at: {self.face_times[ID]}\nName: {profile[1]}\nJob: {profile[2]}\n"
                        cv2.putText(img, f"{profile[1]} ({self.face_times[ID]})", (x, y-40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    else:
                        text = f"Detected at: {self.face_times[ID]}\nName: Unknown\nJob: N/A\n"
                        cv2.putText(img, "Unknown", (x, y-40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                else:
                    text = "Unknown Detected\n"
                    cv2.putText(img, "Unknown", (x, y-40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                info_text += text

            self.userInfo.setText(info_text)  # Update the text area with all current detections

            qt_img = self.convert_cv_qt(img)
            self.imageLabel.setPixmap(qt_img)


    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.imageLabel.width(), self.imageLabel.height(), Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def getprofile(self, ID):
        try:
            connection = mysql.connector.connect(
                host='127.0.0.1',
                database='facesmart',
                user='root',
                
            )
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Emp WHERE ID = %s", (ID,))
            profile = None
            for row in cursor:
                profile = row
            return profile
        except mysql.connector.Error as error:
            print(f"Failed to retrieve profile from database: {error}")
            return None
        finally:
            if connection:
                connection.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FaceRecognitionApp()
    ex.show()
    sys.exit(app.exec_()) 




""" #old code               
import cv2
import numpy as np
import mysql.connector

# Initialize the face detector and the face recognizer.
faceDet = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('recognizer/trainingData.yml')
font = cv2.FONT_HERSHEY_SIMPLEX

def getprofile(ID):
    try:
        # Connect to the database.
        connection = mysql.connector.connect(
            host='127.0.0.1',
            database='facesmart',
            user='root',
            # You might need to add a password parameter here if your DB requires authentication.
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Emp WHERE ID=%s", (ID,))
        profile = None
        for row in cursor:
            profile = row
        return profile
    except mysql.connector.Error as error:
        print(f"Failed to retrieve profile from database: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDet.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
        ID, conf = recognizer.predict(gray[y:y+h, x:x+w])
        profile = getprofile(ID)
        if profile:  # If a profile is found for the recognized face.
            cv2.putText(img, "Name: " + str(profile[1]), (x, y+h+30), font, 1, (0, 255, 0), 2)
            cv2.putText(img, "Job: " + str(profile[2]), (x, y+h+60), font, 1, (0, 255, 0), 2)
        else:  # If no profile is found (unrecognized face).
            cv2.putText(img, "Unknown", (x, y+h+30), font, 1, (0, 255, 0), 2)
    cv2.imshow('Face', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()"""
