
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMessageBox
import cv2
import mysql.connector
import subprocess

class CameraThread(QThread):
    changePixmap = pyqtSignal(QImage)
    captureComplete = pyqtSignal()

    def __init__(self, ID):
        super().__init__()
        self.faceDet = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.ID = ID
        self.sampleNum = 0

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.faceDet.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    self.sampleNum += 1
                    if self.sampleNum <= 20:
                        cv2.imwrite(f"dataSet/user.{self.ID}.{self.sampleNum}.jpg", gray[y:y+h, x:x+w])
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    else:
                        self.captureComplete.emit()
                        cap.release()
                        return
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

class TrainingThread(QThread):
    trainingComplete = pyqtSignal()

    def run(self):
        subprocess.run(['python', 'train.py'], shell=False)
        self.trainingComplete.emit()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 640, 480))
        self.idInput = QtWidgets.QLineEdit(self.centralwidget)
        self.idInput.setGeometry(QtCore.QRect(655, 200, 200, 50))
        self.nameInput = QtWidgets.QLineEdit(self.centralwidget)
        self.nameInput.setGeometry(QtCore.QRect(655, 260, 200, 50))
        self.jobInput = QtWidgets.QLineEdit(self.centralwidget)
        self.jobInput.setGeometry(QtCore.QRect(655, 320, 200, 50))
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(655, 380, 200, 50))
        self.startButton.setText("Start Capture")
        self.startButton.clicked.connect(self.startCapture)

        self.trainButton = QtWidgets.QPushButton(self.centralwidget)
        self.trainButton.setGeometry(QtCore.QRect(655, 440, 200, 50))
        self.trainButton.setText("Train Model")
        self.trainButton.clicked.connect(self.trainModel)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Employee Management System"))

    def startCapture(self):
        ID = self.idInput.text()
        name = self.nameInput.text()
        job = self.jobInput.text()
        if ID and name and job:
            self.insert_update(ID, name, job)
            self.thread = CameraThread(ID)
            self.thread.changePixmap.connect(lambda p: self.label.setPixmap(QPixmap.fromImage(p)))
            self.thread.captureComplete.connect(self.captureFinished)
            self.thread.start()
        else:
            QMessageBox.warning(None, "Input Error", "All fields are required.")

    def insert_update(self, ID, name, job):
        try:
            connection = mysql.connector.connect(host='127.0.0.1', database='facesmart', user='root', password='')
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Emp WHERE ID=%s", (ID,))
            record = cursor.fetchone()
            if record:
                cursor.execute("UPDATE Emp SET Name=%s, Job=%s WHERE ID=%s", (name, job, ID))
            else:
                cursor.execute("INSERT INTO Emp (ID, Name, Job) VALUES (%s, %s, %s)", (ID, name, job))
            connection.commit()
            cursor.close()
            connection.close()
        except mysql.connector.Error as error:
            QMessageBox.critical(None, "Database Error", str(error))

    def captureFinished(self):
        QMessageBox.information(None, "Capture Complete", "Face capture completed successfully.")

    def trainModel(self):
        self.training_thread = TrainingThread()
        self.training_thread.trainingComplete.connect(self.onTrainingComplete)
        self.training_thread.start()

    def onTrainingComplete(self):
        QMessageBox.information(None, "Training Complete", "The training process has completed successfully.")
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())




































"""import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
import cv2
import mysql.connector
import subprocess  # Import subprocess

class CameraThread(QThread):
    changePixmap = pyqtSignal(QImage)
    captureComplete = pyqtSignal()

    def __init__(self, ID):
        super().__init__()
        self.faceDet = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.ID = ID
        self.sampleNum = 0

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.faceDet.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    self.sampleNum += 1
                    if self.sampleNum <= 20:
                        cv2.imwrite(f"dataSet/user.{self.ID}.{self.sampleNum}.jpg", gray[y:y+h, x:x+w])
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    else:
                        self.captureComplete.emit()
                        cap.release()
                        return
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 640, 480))

        self.idInput = QtWidgets.QLineEdit(self.centralwidget)
        self.idInput.setGeometry(QtCore.QRect(655, 200, 200, 50))
        self.idInput.setPlaceholderText("ID")

        self.nameInput = QtWidgets.QLineEdit(self.centralwidget)
        self.nameInput.setGeometry(QtCore.QRect(655, 260, 200, 50))
        self.nameInput.setPlaceholderText("Name")

        self.jobInput = QtWidgets.QLineEdit(self.centralwidget)
        self.jobInput.setGeometry(QtCore.QRect(655, 320, 200, 50))
        self.jobInput.setPlaceholderText("Job")

        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(655, 380, 200, 50))
        self.startButton.setText("Start Capture")
        self.startButton.clicked.connect(self.startCapture)

        self.trainButton = QtWidgets.QPushButton(self.centralwidget)
        self.trainButton.setGeometry(QtCore.QRect(655, 440, 200, 50))
        self.trainButton.setText("Train Model")
        self.trainButton.clicked.connect(self.trainModel)  # Connect the new button

        MainWindow.setCentralWidget(self.centralwidget)

    def startCapture(self):
        ID = self.idInput.text()
        name = self.nameInput.text()
        job = self.jobInput.text()
        self.insert_update(ID, name, job)
        self.thread = CameraThread(ID)
        self.thread.changePixmap.connect(lambda p: self.label.setPixmap(QPixmap.fromImage(p)))
        self.thread.captureComplete.connect(self.captureFinished)
        self.thread.start()

    def insert_update(self, ID, name, job):
        connection = mysql.connector.connect(host='127.0.0.1', database='facesmart', user='root', password='')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Emp WHERE ID=%s", (ID,))
        record = cursor.fetchone()
        if record:
            cursor.execute("UPDATE Emp SET Name=%s, Job=%s WHERE ID=%s", (name, job, ID))
        else:
            cursor.execute("INSERT INTO Emp (ID, Name, Job) VALUES (%s, %s, %s)", (ID, name, job))
        connection.commit()
        cursor.close()
        connection.close()

    def captureFinished(self):
        print("Capture complete.")

    def trainModel(self):
        # Run the train.py script
        subprocess.Popen(['python', 'train.py'], shell=False)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())"""
