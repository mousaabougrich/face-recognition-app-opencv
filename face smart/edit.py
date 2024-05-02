import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog
from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector
from mysql.connector import Error

class Ui_EditEmployeeWindow(object):
    def setupUi(self, EditEmployeeWindow):
        EditEmployeeWindow.setObjectName("EditEmployeeWindow")
        EditEmployeeWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(EditEmployeeWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(270, 40, 351, 61))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 170, 271, 51))
        font = QtGui.QFont()
        font.setFamily("Sakkal Majalla")
        font.setPointSize(22)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 240, 271, 51))
        font = QtGui.QFont()
        font.setFamily("Sakkal Majalla")
        font.setPointSize(22)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 310, 271, 51))
        font = QtGui.QFont()
        font.setFamily("Sakkal Majalla")
        font.setPointSize(22)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.textEdit_id = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_id.setGeometry(QtCore.QRect(310, 170, 171, 41))
        self.textEdit_id.setObjectName("textEdit_id")
        self.textEdit_new_name = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_new_name.setGeometry(QtCore.QRect(310, 240, 171, 41))
        self.textEdit_new_name.setObjectName("textEdit_new_name")
        self.textEdit_new_job = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_new_job.setGeometry(QtCore.QRect(310, 310, 171, 41))
        self.textEdit_new_job.setObjectName("textEdit_new_job")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(320, 400, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Pristina")
        font.setPointSize(18)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        EditEmployeeWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(EditEmployeeWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        EditEmployeeWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(EditEmployeeWindow)
        self.statusbar.setObjectName("statusbar")
        EditEmployeeWindow.setStatusBar(self.statusbar)

        self.retranslateUi(EditEmployeeWindow)
        QtCore.QMetaObject.connectSlotsByName(EditEmployeeWindow)

    def retranslateUi(self, EditEmployeeWindow):
        _translate = QtCore.QCoreApplication.translate
        EditEmployeeWindow.setWindowTitle(_translate("EditEmployeeWindow", "Edit Employee"))
        self.label.setText(_translate("EditEmployeeWindow", "EDIT EMPLOYEE"))
        self.label_2.setText(_translate("EditEmployeeWindow", "ENTER EMPLOYEE ID:"))
        self.label_3.setText(_translate("EditEmployeeWindow", " EMPLOYEE NAME:"))
        self.label_4.setText(_translate("EditEmployeeWindow", "EMPLOYEE JOB:"))
        self.pushButton.setText(_translate("EditEmployeeWindow", "Edit"))

class EditEmployeeWindow(QMainWindow):
    def __init__(self):
        super(EditEmployeeWindow, self).__init__()
        self.ui = Ui_EditEmployeeWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.edit_employee)

    def edit_employee(self):
        emp_id = self.ui.textEdit_id.toPlainText()
        new_name = self.ui.textEdit_new_name.toPlainText()
        new_job = self.ui.textEdit_new_job.toPlainText()
        try:
            connection = mysql.connector.connect(host='127.0.0.1',
                                                 database='facesmart',
                                                 user='root'
                                                 )
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(f"UPDATE emp SET Name='{new_name}', Job='{new_job}' WHERE Id={emp_id}")
                connection.commit()
                QtWidgets.QMessageBox.information(self, "Success", "Employee information updated successfully!")
                cursor.close()
        except Error as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error occurred: {str(e)}")
        finally:
            if connection.is_connected():
                connection.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EditEmployeeWindow()
    window.show()
    sys.exit(app.exec_())
