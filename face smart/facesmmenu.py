from PyQt5 import QtCore, QtGui, QtWidgets
from facesm import Ui_Dialog
import subprocess  # Import subprocess

class Ui_MENU(object):
    def openwindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.window)
        self.window.show()

    def run_detector(self):
        # Runs the detectore.py script
        subprocess.Popen(['python', 'detectore.py'], shell=False)
        
    def setupUi(self, MENU):
        MENU.setObjectName("MENU")
        MENU.resize(800, 527)
        self.centralwidget = QtWidgets.QWidget(MENU)
        self.centralwidget.setObjectName("centralwidget")
        
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(0, -10, 801, 501))
        self.tableView.setObjectName("tableView")
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(310, 50, 391, 61))
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT Condensed Extra Bold")
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.openwindow())
        self.pushButton.setGeometry(QtCore.QRect(100, 210, 111, 71))
        self.pushButton.setStyleSheet("QPushButton {\n"
"    background-color: #4CAF50; \n"
"    border: none;\n"
"    color: white;\n"
"    padding: 10px 20px;\n"
"    text-align: center;\n"
"    text-decoration: none;\n"
"    display: inline-block;\n"
"    font-size: 20px;\n"
"    margin: 4px 2px;\n"
"    cursor: pointer;\n"
"    border-radius: 8px;\n"
"}\n")
        self.pushButton.setObjectName("pushButton")
        
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.run_detector())
        self.pushButton_2.setGeometry(QtCore.QRect(590, 210, 131, 71))
        self.pushButton_2.setStyleSheet("QPushButton {\n"
"    background-color: #4CAF50; \n"
"    border: none;\n"
"    color: white;\n"
"    padding: 10px 20px;\n"
"    text-align: center;\n"
"    text-decoration: none;\n"
"    display: inline-block;\n"
"    font-size: 20px;\n"
"    margin: 4px 2px;\n"
"    cursor: pointer;\n"
"    border-radius: 8px;\n"
"}\n")
        self.pushButton_2.setObjectName("pushButton_2")
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 30, 231, 101))
        self.label_2.setPixmap(QtGui.QPixmap("../logo-1.png"))  # Ensure the path to your image is correct
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        
        MENU.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MENU)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MENU.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MENU)
        self.statusbar.setObjectName("statusbar")
        MENU.setStatusBar(self.statusbar)

        self.retranslateUi(MENU)
        QtCore.QMetaObject.connectSlotsByName(MENU)

    def retranslateUi(self, MENU):
        _translate = QtCore.QCoreApplication.translate
        MENU.setWindowTitle(_translate("MENU", "MainWindow"))
        self.label.setText(_translate("MENU", "MENU"))
        self.pushButton.setText(_translate("MENU", "ADMIN"))
        self.pushButton_2.setText(_translate("MENU", "EMPLOYEE"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MENU = QtWidgets.QMainWindow()
    ui = Ui_MENU()
    ui.setupUi(MENU)
    MENU.show()
    sys.exit(app.exec_())



