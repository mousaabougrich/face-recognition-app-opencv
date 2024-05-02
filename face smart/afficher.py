import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector
from mysql.connector import Error

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtWidgets.QTableWidget(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(5, 1, 791, 541))
        self.tableView.setObjectName("tableView")
        self.tableView.setColumnCount(3)  
        self.tableView.setHorizontalHeaderLabels(["ID", "Name", "Job"])  
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(330, 560, 141, 31))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Display Employees"))

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.display_employees)

    def display_employees(self):
        try:
            connection = mysql.connector.connect(host='127.0.0.1',
                                                 database='facesmart',
                                                 user='root'
                                                 )
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT id, name, job FROM emp")
                employees = cursor.fetchall()
                self.ui.tableView.setRowCount(len(employees))
                for row_index, employee in enumerate(employees):
                    for col_index, data in enumerate(employee):
                        self.ui.tableView.setItem(row_index, col_index, QTableWidgetItem(str(data)))
                cursor.close()
        except Error as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error occurred: {str(e)}")
        finally:
            if connection.is_connected():
                connection.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
