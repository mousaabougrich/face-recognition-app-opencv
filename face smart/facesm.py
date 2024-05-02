from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import mysql.connector
import subprocess  # Import subprocess
from PyQt5.QtWidgets import QMessageBox

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(957, 649)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(-10, 0, 961, 651))
        self.widget.setStyleSheet("background-color:white")
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(240, 10, 491, 81))
        self.label.setAutoFillBackground(False)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("logo-1.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(340, 120, 281, 81))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.textEdit = QtWidgets.QLineEdit(self.widget)
        self.textEdit.setGeometry(QtCore.QRect(320, 240, 301, 61))
        self.textEdit.setStyleSheet("...")
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setPlaceholderText("ENTRER VOTRE NOM")
        self.textEdit.textChanged.connect(self.updateNamePlaceholder)
        self.textEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.textEdit_2.setGeometry(QtCore.QRect(320, 340, 301, 61))
        self.textEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)  
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.setPlaceholderText("ENTRER LE MOT DE PASSE")
        self.textEdit_2.textChanged.connect(self.updatePasswordPlaceholder)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(410, 450, 121, 71))
        font = QtGui.QFont()
        font.setPointSize(12) 
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("...")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.login)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "ADMIN LOGIN "))
        self.pushButton.setText(_translate("Dialog", "LOGIN "))

    def updateNamePlaceholder(self):
        if self.textEdit.text():
            self.textEdit.setPlaceholderText("")
        else:
            self.textEdit.setPlaceholderText("ENTRER VOTRE NOM")

    def updatePasswordPlaceholder(self):
        if self.textEdit_2.text():
            self.textEdit_2.setPlaceholderText("")
        else:
            self.textEdit_2.setPlaceholderText("ENTRER LE MOT DE PASSE")

    def login(self):
        username = self.textEdit.text().strip()
        password = self.textEdit_2.text().strip()

        try:
            connection = mysql.connector.connect(host='127.0.0.1',
                                                 database='facesmart',
                                                 user='root')
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM admin WHERE name = %s AND Password = %s", (username, password))
                user = cursor.fetchone()

                if user:
                    QMessageBox.information(None, "Success", "Login Successful")
                    subprocess.Popen(['python', 'gestion.py'], shell=False)  # Execute gestion.py after successful login
                else:
                    QMessageBox.critical(None, "Error", "Invalid username or password")

                cursor.close()
            else:
                QMessageBox.critical(None, "Error", "Failed to connect to database")

        except mysql.connector.Error as error:
            QMessageBox.critical(None, "Error", f"Failed to connect to database: {error}")

        finally:
            if 'connection' in locals():
                connection.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
