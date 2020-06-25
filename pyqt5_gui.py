import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("My Awesome App")

        layout_main = QGridLayout()
        layout_title = QHBoxLayout()
        layout_userName = QHBoxLayout()
        layout_password = QHBoxLayout()
        layout_message = QHBoxLayout()

        ### FIRST ROW ###
        title = QLabel("Bot for Instagram automation")
        title.setStyleSheet("font: 45px Berlin Sans FB Demi;"
                            "font-weight: bold;"
                            "color: #00000;"
                            "border: 2px solid black;")
        font = title.font() # Objekt
        font.setLetterSpacing(QFont.AbsoluteSpacing,4)
        title.setFont(font)
        title.setAlignment(Qt.AlignCenter)
        labelPhoto = QLabel()
        picPhoto = QPixmap("inst_photo.png")
        picPhoto = picPhoto.scaled(150,150,Qt.KeepAspectRatio, Qt.FastTransformation)
        labelPhoto.setPixmap(picPhoto)
        labelPhoto.setAlignment(Qt.AlignCenter)
        layout_title.addWidget(title)
        layout_title.addWidget(labelPhoto)

        layout_main.addLayout(layout_title,0,0)

        ### Second Row ######
        loginText = QLabel("Login Instagram")
        loginText.setStyleSheet("font: 40px Berlin Sans FB Demi;"
                                "font-weight: bold;"
                                "color: #00000")
        layout_main.addWidget(loginText)

        ###################################
        ### Third ROW ######
        usernameText = QLabel("Username")
        usernameText.setStyleSheet("font: 35px Arial;"
                                   "font-weight: normal;")
        usernameText.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout_userName.addWidget(usernameText)

        usernameInput = QTextEdit()
        usernameInput.setStyleSheet("font: 35px Arial;"
                                   "font-weight: normal;")
        usernameInput.setContentsMargins(50,0,10,0)
        usernameInput.setFixedHeight(50)

        layout_userName.addWidget(usernameInput)
        layout_userName.setContentsMargins(0,20,0,5)
        layout_main.addLayout(layout_userName,2,0)

        ######     Fourth Row       #######
        passwordText = QLabel("Password")
        passwordText.setStyleSheet("font: 35px Arial;"
                                   "font-weight: normal;")
        layout_password.addWidget(passwordText)


        layout_main.addLayout(layout_password,3,0)
        layout_main.setContentsMargins(10,0,10,0)

        widget = QWidget() # LADER DER KOMMER SYSTEM INPUT
        widget.setLayout(layout_main)

        self.setCentralWidget(widget) # GØR AT WIDGET ER MAIN TING





app=QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()