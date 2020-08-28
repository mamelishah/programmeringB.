import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QPushButton
import time

import index

botObject = index.bot()
usernameText = None
passwordText = None
valueCheckBox = None
done = False

styleSheet_mainWindow = "QLabel#label {font: 45px Berlin Sans FB Demi;" \
                        "font-weight: bold;" \
                        "color: black;}" \
                        "QLabel#usernameText, QLabel#passwordText  {font: 20px Arial; color: #5baaea; border: 2px solid rgb(91,170,234); border-radius: 10px; " \
                        "background-color: rgb(255,255,255); font-weight: bold;}" \
                        "QLineEdit#usernameInput, QLineEdit#passwordInput {border: 1px solid rgb(91,170,234); border-radius:10px; background-color: palette(base);" \
                        "font: 40px Arial;}" \
                        "QLineEdit#usernameInput:focus, QLineEdit#passwordInput:focus {border: 2px solid rgb(91,170,234);} " \
                        "QPushButton#buttonLogin {border: 2px solid #5baaea; border-radius:20px; background-color: palette(base); font-weight: bold; font-size: 20px; color:#5baaea }" \
                        "MainWindow {background-color: white}" \
                        "QCheckBox#checkBoxWindowVisible::indicator {height: 25px; width: 25px;}" \
 \
    styleSheet_dialog = "QPushButton#buttonOk {border: 2px solid grey; border-radius:20px; background-color: palette(base);}" \
                        "QPushButton#buttonOk:hover {border: 2px solid #5baaea;}" \
                        "QLabel {font: 25px Arial;font-weight: bold;}"


class CustomDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)
        loadImg = "errorImage.png"

        self.setWindowTitle("error")
        self.setFixedSize(400, 150)

        layout_main = QVBoxLayout()
        layout_firstRow = QHBoxLayout()
        layout_secondRow = QHBoxLayout()
        layout_thirdRow = QHBoxLayout()

        self.errorImg = QLabel(self)
        pixmap = QPixmap(loadImg)
        pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio)
        self.errorImg.setPixmap(pixmap)

        self.errorText = QLabel("Failed login", self)

        self.errorTextMore = QLabel("Please try again", self)

        self.buttonOk = QPushButton("OK", self)
        self.buttonOk.setFixedSize(70, 40)
        self.buttonOk.setObjectName("buttonOk")

        layout_firstRow.addWidget(self.errorImg)
        layout_firstRow.addWidget(self.errorText)
        layout_firstRow.setAlignment(Qt.AlignLeft)

        layout_secondRow.addWidget(self.errorTextMore)
        layout_secondRow.setContentsMargins(67, 0, 0, 0)

        layout_thirdRow.addWidget(self.buttonOk)
        layout_thirdRow.setAlignment(Qt.AlignRight)

        layout_main.addLayout(layout_firstRow)
        layout_main.addLayout(layout_secondRow)
        layout_main.addLayout(layout_thirdRow)

        self.setStyleSheet(styleSheet_dialog)
        self.setLayout(layout_main)

    def paintEvent(self, event):
        bg_rect_title = QPainter(self)
        bg_rect_title.setPen(QPen(Qt.lightGray, 2, Qt.SolidLine))
        bg_rect_title.setBrush(QBrush(QColor.fromRgb(255, 255, 255), Qt.SolidPattern))
        bg_rect_title.drawRoundedRect(10, 8, 380, 135, 7, 7)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Instagram Automation")
        self.setFixedSize(750, 620)
        self.setWindowIcon(QIcon("inst_photo.png"))
        self.setObjectName("window")

        self.setStyleSheet(styleSheet_mainWindow)

        self.passwordInput = None
        self.userNameInput = None
        self.checkBoxWindowVisible = None
        self.prog = ProgressBarDemo()
        self.worker = Worker()
        self.workerData = WorkerData()

        self.worker.started.connect(self.started_login)
        self.worker.finished.connect(self.finished_login)
        self.workerData.finished.connect(self.dataLoadingFinished)

        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.updateProgress)
        self.counter = 0
        self.UI()

    def dataLoadingFinished(self):
        self.close()
        self.prog.close()

    def finished_login(self):
        self.timer.stop()
        if (botObject.error_login):
            self.dd = CustomDialog()
            self.dd.buttonOk.clicked.connect(self.buttonErrorButton)
            self.dd.exec_()
        else:
            del self.worker
            self.timer.start()
            self.prog.infoLAbel.setText("Loading Data")
            self.updateProgress()
            self.workerData.start()

    def buttonErrorButton(self):
        self.dd.close()
        self.passwordInput.setText("")
        self.usernameInput.setText("")
        self.show()

    def started_login(self):
        self.hide()
        self.prog.show()
        self.timer.start()
        self.updateProgress()

    def updateProgress(self):
        if (self.counter <= 100):
            self.counter += 1
            self.prog.progBar.setValue(self.counter)
        else:
            self.counter = 0

    def paintEvent(self, Event):
        bg_rect_title = QPainter(self)
        bg_rect_title.setPen(QPen(QColor.fromRgb(91, 170, 234), 2, Qt.SolidLine))
        bg_rect_title.setBrush(QBrush(QColor.fromRgb(255, 255, 255), Qt.SolidPattern))
        bg_rect_title.drawRoundedRect(10, 10, 730, 76, 7, 7)

        bg_rect = QPainter(self)
        bg_rect.setPen(QPen(QColor.fromRgb(91, 170, 234), 2, Qt.SolidLine))
        bg_rect.setBrush(QBrush(QColor.fromRgb(255, 255, 255), Qt.SolidPattern))
        bg_rect.drawRoundedRect(10, 95, 730, 220, 7, 7)

        bg_rect_bottom = QPainter(self)
        bg_rect_bottom.setPen(QPen(QColor.fromRgb(91, 170, 234), 2, Qt.SolidLine))
        bg_rect_bottom.setBrush(QBrush(QColor.fromRgb(255, 255, 255), Qt.SolidPattern))
        bg_rect_bottom.drawRoundedRect(10, 325, 730, 220, 7, 7)

    def UI(self):

        ########### TITLE ############
        label = QLabel('Bot For Instagram Automation', self)
        label.setObjectName("label")
        fontT = label.font()
        fontT.setLetterSpacing(QFont.AbsoluteSpacing, 3)
        label.setFont(fontT)
        label.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        label.resize(730, 60)
        label.move(10, 10)

        #################################
        ###### LOGIN ###################

        loginText = QLabel('Login Instagram', self)
        loginText.setStyleSheet("font: 30px Arial;"
                                "font-weight: bold;"
                                "color: black;")
        fontl = loginText.font()
        fontl.setLetterSpacing(QFont.AbsoluteSpacing, 3)
        loginText.setFont(fontl)

        loginText.resize(670, 60)
        loginText.move(20, 90)

        usernameText = QLabel('Username', self)
        usernameText.setObjectName("usernameText")
        fontU = usernameText.font()
        fontU.setLetterSpacing(QFont.AbsoluteSpacing, 2.5)
        usernameText.setFont(fontU)
        usernameText.setAlignment(Qt.AlignCenter)
        usernameText.resize(130, 60)
        usernameText.move(20, 160)

        self.usernameInput = QLineEdit(self)
        self.usernameInput.setObjectName("usernameInput")
        self.usernameInput.setContentsMargins(0, 0, 0, 0)
        self.usernameInput.setPlaceholderText("Username")
        self.usernameInput.setText("")
        self.usernameInput.resize(450, 60)
        self.usernameInput.move(160, 160)

        passwordText = QLabel('Password', self)
        passwordText.setObjectName("passwordText")
        passwordText.setFrameShadow(QFrame.Plain)
        passwordText.setAlignment(Qt.AlignCenter)
        passwordText.resize(130, 60)
        passwordText.move(20, 240)

        self.passwordInput = QLineEdit(self)
        self.passwordInput.setObjectName("passwordInput")
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.passwordInput.setContentsMargins(0, 0, 0, 0)
        self.passwordInput.setPlaceholderText("Password")
        self.passwordInput.setText("")
        self.passwordInput.resize(450, 60)
        self.passwordInput.move(160, 240)

        #################################
        ## Info ######################
        text = QLabel(
            "This software is made for increasing business acounts' activities on the \nsocial media Instagram. The program is "
            "not meant to be a spam software \nfor Instagram, but to make a account grow in a natural way. "
            "All use of this\nsoftware is at your own risk. ", self)

        text.setStyleSheet("font: 20px Arial; color: #000000; font-weight: bold")
        text.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        text.resize(700, 200)
        text.move(20, 330)

        textStrong = QLabel(
            "The founder of this software takes no responsibility \nfor blocking your account on instagram", self)
        textStrong.setStyleSheet("font: 20px Arial; color: #FF0000; font-weight: bold")
        textStrong.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        textStrong.resize(600, 200)
        textStrong.move(20, 440)

        textAuthor = QLabel(
            "This software is provided and made by Mohammad R.", self)
        textAuthor.setStyleSheet("font: 20px Arial; color: #000000; font-weight: bold")
        textAuthor.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        textAuthor.resize(600, 200)
        textAuthor.move(20, 510)

        buttonLogin = QPushButton("Login", self)
        buttonLogin.setObjectName("buttonLogin")
        buttonLogin.clicked.connect(self.on_click)
        buttonLogin.resize(120, 60)
        buttonLogin.move(617, 555)

        checkBoxText = QLabel("Invisible browser", self)
        checkBoxText.setStyleSheet("color: #5baaea")
        checkBoxText.resize(100, 50)
        checkBoxText.move(507, 570)

        self.checkBoxWindowVisible = QCheckBox(self)
        self.checkBoxWindowVisible.setObjectName("checkBoxWindowVisible")
        self.checkBoxWindowVisible.resize(30, 30)
        self.checkBoxWindowVisible.move(480, 580)

        self.show()
        self.setFocus()

    def on_click(self):
        global valueCheckBox
        global usernameText
        global passwordText

        valueCheckBox = self.checkBoxWindowVisible.isChecked()
        usernameText = self.usernameInput.text()
        passwordText = self.passwordInput.text()

        self.worker.start()


class ProgressBarDemo(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(ProgressBarDemo, self).__init__(*args, **kwargs)
        self.setStyleSheet("background-color: white")

        self.setFixedSize(300, 140)
        self.setWindowTitle("Loading")

        layout_main = QGridLayout()
        layout_firstRow = QHBoxLayout()
        layout_secondRow = QHBoxLayout()

        self.text = QLabel("Loading...", self)
        #  self.text.setAlignment(Qt.AlignCenter)
        self.text.setStyleSheet("QLabel {font: 25px Arial black; font-weight: bold;}")
        self.text.setAlignment(Qt.AlignCenter)

        self.progBar = QProgressBar(self)
        # self.progBar.setAlignment(Qt.AlignCenter)
        self.progBar.setTextVisible(False)

        layout_firstRow.addWidget(self.text)
        layout_secondRow.addWidget(self.progBar)

        layout_main.addLayout(layout_firstRow, 0, 0)

        self.infoLAbel = QLabel(self)
        self.infoLAbel.setText("Login in..")
        self.infoLAbel.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("font: 20px Arial; color: black; font-weight: bold")
        layout_main.addWidget(self.infoLAbel, 1, 0)

        layout_main.addLayout(layout_secondRow, 2, 0)

        window = QWidget()
        window.setLayout(layout_main)
        self.setCentralWidget(window)


class Worker(QThread):

    @pyqtSlot()
    def run(self):
        self.mutex = QMutex()
        self.mutex.lock()
        botObject.login(usernameText, passwordText, valueCheckBox)
        self.mutex.unlock()


class WorkerData(QThread):

    @pyqtSlot()
    def run(self):
        self.mutex = QMutex()
        self.mutex.lock()
        botObject.send_own_data_csv()
        botObject.save_information_csv()
        botObject.unfollower()
        self.mutex.unlock()


app = QApplication(sys.argv)
window = MainWindow()
app.exec_()

del app
del window

followValue = None
likeValue = None
commentValue = None

boysValue = None
girlsValue = None

lang_1Value = None
lang_2Value = None
lang_3Value = None
lang_4Value = None

hashtagValueList = None

commentValueList = None

if (botObject.login_success):
    username = botObject.username
    followers = len(botObject.followers_list)
    following = len(botObject.following_list)

    tuplesWithCountries = ["None", "All", "English", "Danish", "Spanish", "German", "Swedish", "French", "Russian",
                           "Italian", "Chinese", "Portuguese"]

    styleSettingWindow = "QLabel#usernameText, QLabel#usernameTitle {font: 40px Arial; font-weight: bold; color:rgb(91, 170, 234);}" \
                         "QLabel#usernameTitle {color: black}" \
                         "QLabel#textInfo, QLabel#settingTitle {font: 28px Arial; font-weight: bold; color: rgb(91, 170, 234);}" \
                         "QLabel#followNr {font: 22px Arial; font-weight: bold;; }" \
                         "QLabel#settingFunctions,QLabel#genderPick, QLabel#languagePick, QLabel#hashtagPick, QLabel#commentPick {font: 24px Arial; font-weight: bold; text-decoration: underline;}" \
                         "QPushButton#launchButton {border: 2px solid #5baaea; border-radius:20px; background-color: palette(base);}" \
                         "QPushButton#launchButton:hover {border: 3px solid #5baaea;}"


    class settingWindow(QMainWindow):
        def __init__(self, parent=None):
            super(settingWindow, self).__init__(parent)
            self.UISetting()
            self.setStyleSheet(styleSettingWindow)
            self.launchButton.clicked.connect(self.launcherHandler)

        def filterHastag(self, stringText):

            string = stringText.replace(" ", "")
            start = 0
            end = 0
            listHashtags = []
            dicts = {}

            for n in range(len(string)):
                if (string[n] == "["):
                    start = n + 1

                elif (string[n] == ":"):
                    end = n
                    hashtag = string[start:end]
                    listHashtags.append(hashtag)

                if (string[n] == ":"):
                    start = n + 1

                elif (string[n] == "]"):
                    end = n
                    weight = string[start:end]
                    listHashtags.append(weight)

            try:
                dicts = {listHashtags[i]: int(listHashtags[i + 1]) for i in range(0, len(listHashtags), 2)}
            except:
                self.errorMessage = QMessageBox(self)
                self.errorMessage.setText("ERROR -> Check hashtag selecting")
                self.errorMessage.exec()
                return "ERROR"
            finally:
                return dicts

        def filterComment(self, comment):
            start = 0
            end = 0

            list_comment = []

            for m in range(len(comment)):
                if (comment[m] == "["):
                    start = m + 1

                elif (comment[m] == "]"):
                    end = m
                    list_comment.append(comment[start:end])
                    start = 0
                    end = 0

            return list_comment

        def launcherHandler(self):
            followValue = self.checkBoxFollow.isChecked()
            likeValue = self.checkBoxLike.isChecked()
            commentValue = self.checkBoxComment.isChecked()

            boysValue = self.checkBoxBoys.isChecked()
            girlsValue = self.checkBoxBoys.isChecked()

            langList = []

            for s in self.lang_holder.values():
                s = s.currentText()

                if (s == "All"):
                    langList = list(tuplesWithCountries)
                    langList.remove("None")
                    langList.remove("All")
                    break

                elif (s == "None" or s == None):
                    continue

                elif (s not in langList):
                    langList.append(s)

            hashtagValueList = self.hashtagField.toPlainText()
            commentValueList = self.commentField.toPlainText()

            hashtagDict = self.filterHastag(hashtagValueList)

            commentValueList = self.filterComment(commentValueList)

            self.workerT = workerLaunch(hashtagDict, followValue, likeValue, langList, girlsValue, boysValue,
                                        commentValue, commentValueList)
            self.workerT.start()

        def paintEvent(self, Event):
            bg_rect_title = QPainter(self)
            bg_rect_title.setPen(QPen(QColor.fromRgb(91, 170, 234), 2, Qt.SolidLine))
            bg_rect_title.setBrush(QBrush(QColor.fromRgb(255, 255, 255), Qt.SolidPattern))
            bg_rect_title.drawRoundedRect(8, 10, 835, 76, 7, 7)

            bg_rect_info = QPainter(self)
            bg_rect_info.setPen(QPen(QColor.fromRgb(91, 170, 234), 2, Qt.SolidLine))
            bg_rect_info.setBrush(QBrush(QColor.fromRgb(255, 255, 255), Qt.SolidPattern))
            bg_rect_info.drawRoundedRect(8, 95, 835, 110, 7, 7)

            bg_rect_setting = QPainter(self)
            bg_rect_setting.setPen(QPen(QColor.fromRgb(91, 170, 234), 2, Qt.SolidLine))
            bg_rect_setting.setBrush(QBrush(QColor.fromRgb(255, 255, 255), Qt.SolidPattern))
            bg_rect_setting.drawRoundedRect(8, 215, 835, 450, 7, 7)

        def UISetting(self):
            self.setFixedSize(850, 700)

            self.setWindowTitle("Settings")

            usernameText = QLabel("Username:", self)
            fontUS = usernameText.font()
            fontUS.setLetterSpacing(QFont.AbsoluteSpacing, 2)
            usernameText.setFont(fontUS)
            usernameText.resize(550, 100)
            usernameText.setObjectName("usernameText")
            usernameText.move(15, 1)

            usernameTitle = QLabel(username, self)
            fontUS = usernameTitle.font()
            fontUS.setLetterSpacing(QFont.AbsoluteSpacing, 2)
            usernameTitle.setFont(fontUS)
            usernameTitle.resize(550, 100)
            usernameTitle.setObjectName("usernameTitle")
            usernameTitle.move(250, 1)

            textinfo = QLabel("Account data", self)
            textinfo.resize(200, 40)
            fontIn = textinfo.font()
            fontIn.setLetterSpacing(QFont.AbsoluteSpacing, 2)
            textinfo.setFont(fontIn)
            textinfo.setObjectName("textInfo")
            textinfo.move(15, 100)

            followersNrString = "Followers: {}".format(followers)
            followersNr = QLabel(followersNrString, self)
            followersNr.resize(165, 45)
            followersNr.setObjectName("followNr")
            followersNr.move(15, 150)

            followingNrString = "Following: {}".format(following)
            followingNr = QLabel(followingNrString, self)
            followingNr.setAlignment(Qt.AlignCenter)
            followingNr.resize(165, 45)
            followingNr.setObjectName("followNr")
            followingNr.move(200, 150)

            followersCSVText = QLabel("Open 'Followers' CSV file", self)
            followersCSVText.resize(180, 100)
            followersCSVText.setObjectName("followersCSVText")
            followersCSVText.move(570, 130)

            openFollowersCSV = QPushButton("Open", self)
            openFollowersCSV.setFixedSize(70, 30)
            openFollowersCSV.setObjectName("openFollowersCSV")
            openFollowersCSV.move(750, 165)

            followingCSVText = QLabel("Open 'Following' CSV file", self)
            followingCSVText.resize(180, 100)
            followingCSVText.setObjectName("followingCSVText")
            followingCSVText.move(570, 95)

            openFollowingCSV = QPushButton("Open", self)
            openFollowingCSV.setFixedSize(70, 30)
            openFollowingCSV.setObjectName("openFollowingCSV")
            openFollowingCSV.move(750, 130)

            settingTitle = QLabel("Settings", self)
            settingTitle.resize(120, 100)
            settingTitle.setObjectName("settingTitle")
            settingTitle.move(15, 190)

            settingFunctions = QLabel("Functions", self)
            settingFunctions.resize(120, 70)
            settingFunctions.setObjectName("settingFunctions")
            settingFunctions.move(15, 240)

            self.checkBoxFollow = QCheckBox("Follow", self)
            self.checkBoxFollow.move(50, 310)

            self.checkBoxLike = QCheckBox("Like", self)
            self.checkBoxLike.move(160, 310)

            self.checkBoxComment = QCheckBox("Comment", self)
            self.checkBoxComment.move(250, 310)

            genderPick = QLabel("Gender", self)
            genderPick.resize(120, 65)
            genderPick.setObjectName("genderPick")
            genderPick.move(15, 330)

            self.checkBoxBoys = QCheckBox("Boys", self)
            self.checkBoxBoys.move(50, 390)

            self.checkBoxGirls = QCheckBox("Girls", self)
            self.checkBoxGirls.move(160, 390)

            languagePick = QLabel("Language", self)
            languagePick.resize(120, 60)
            languagePick.setObjectName("languagePick")
            languagePick.move(15, 410)

            self.lang_holder = {}

            for x in range(4):
                self.lang_holder["lang_" + str(x)] = QComboBox(self)
                self.lang_holder["lang_" + str(x)].resize(100, 30)
                self.lang_holder["lang_" + str(x)].setPlaceholderText("None")
                self.lang_holder["lang_" + str(x)].addItems(tuplesWithCountries)
                self.lang_holder["lang_" + str(x)].move(50 + x * 130, 470)

            hashtagPick = QLabel("Pick hashtag -> [hashtag:weight]", self)
            hashtagPick.resize(250, 65)
            hashtagPick.setObjectName("hashtagPick")
            hashtagPick.move(15, 495)

            self.hashtagField = QTextEdit(self)
            self.hashtagField.resize(350, 100)
            self.hashtagField.move(15, 560)

            commentPick = QLabel("Pick comment", self)
            commentPick.resize(190, 65)
            commentPick.setObjectName("commentPick")
            commentPick.move(380, 495)

            self.commentField = QTextEdit(self)
            self.commentField.resize(350, 100)
            self.commentField.move(380, 560)

            self.launchButton = QPushButton("Launch", self)
            self.launchButton.setFixedSize(100, 50)
            self.launchButton.setObjectName("launchButton")
            self.launchButton.move(735, 610)

            self.show()


    class workerLaunch(QThread):

        def __init__(self, dict_has, follow, like, lang, girl, boys, comment, commentList):
            super(workerLaunch, self).__init__()

            self.mutex = QMutex()

            self.hashtag_dict = dict_has
            self.follow = follow
            self.like = like
            self.langList = lang
            self.girlValue = girl
            self.boyValue = boys
            self.comment = comment
            self.commentList = commentList

        @pyqtSlot()
        def run(self):
            self.mutex.lock()
            botObject.tagFinder(self.hashtag_dict, self.follow, self.like, self.langList, self.girlValue, self.boyValue,
                                self.comment, self.commentList)
            self.mutex.unlock()


    app = QApplication(sys.argv)
    windowSetting = settingWindow()
    app.exec_()
