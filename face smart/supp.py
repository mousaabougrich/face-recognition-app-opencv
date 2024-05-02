import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog
from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector
from mysql.connector import Error

class Ui_DeleteEmployeeWindow(object):
    def setupUi(self, DeleteEmployeeWindow):
        DeleteEmployeeWindow.setObjectName("DeleteEmployeeWindow")
        DeleteEmployeeWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(DeleteEmployeeWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(5, 1, 801, 571))
        self.tableView.setObjectName("tableView")
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
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(310, 170, 171, 41))
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(320, 350, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Pristina")
        font.setPointSize(18)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        DeleteEmployeeWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(DeleteEmployeeWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        DeleteEmployeeWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(DeleteEmployeeWindow)
        self.statusbar.setObjectName("statusbar")
        DeleteEmployeeWindow.setStatusBar(self.statusbar)

        self.retranslateUi(DeleteEmployeeWindow)
        QtCore.QMetaObject.connectSlotsByName(DeleteEmployeeWindow)

    def retranslateUi(self, DeleteEmployeeWindow):
        _translate = QtCore.QCoreApplication.translate
        DeleteEmployeeWindow.setWindowTitle(_translate("DeleteEmployeeWindow", "Delete Employee"))
        self.label.setText(_translate("DeleteEmployeeWindow", "SUPPRIMER EMPLOYE"))
        self.label_2.setText(_translate("DeleteEmployeeWindow", "ENTRER ID EMPLOYE:"))
        self.pushButton.setText(_translate("DeleteEmployeeWindow", "supprimer"))

class DeleteEmployeeWindow(QMainWindow):
    def __init__(self):
        super(DeleteEmployeeWindow, self).__init__()
        self.ui = Ui_DeleteEmployeeWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.delete_employee)

    def delete_employee(self):
        emp_id = self.ui.textEdit.toPlainText()
        try:
            connection = mysql.connector.connect(host='127.0.0.1',
                                                 database='facesmart',
                                                 user='root'
                                                 )
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(f"DELETE FROM emp WHERE id={emp_id}")
                connection.commit()
                QtWidgets.QMessageBox.information(self, "Success", "Employee deleted successfully!")
                cursor.close()
        except Error as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error occurred: {str(e)}")
        finally:
            if connection.is_connected():
                connection.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeleteEmployeeWindow()
    window.show()
    sys.exit(app.exec_())
