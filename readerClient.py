# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test3.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtWidgets
import sys
import socket
import ast

HOST = '127.0.0.1'
PORT = 65432
nowChapter = 1
nowPage = 1
chapterNumber = 1
pageNumber = 1
Directory = {}
Bookmark = []

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1123, 780)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 20, 1101, 641))
        self.textBrowser.setObjectName("textBrowser")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(180, 680, 46, 22))
        self.spinBox.setObjectName("spinBox")
        self.spinBox_2 = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_2.setGeometry(QtCore.QRect(60, 680, 46, 21))
        self.spinBox_2.setObjectName("spinBox_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 680, 72, 15))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(140, 680, 72, 15))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(790, 680, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(900, 680, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(480, 680, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(310, 680, 161, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")   # ???????????????

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(270, 680, 72, 15))
        self.label_3.setObjectName("label_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(680, 680, 93, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1123, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # chapter and page
        self.spinBox_2.setRange(1, chapterNumber)
        self.spinBox.setRange(1, pageNumber)
        self.spinBox_2.valueChanged.connect(self.changechapterNumber)
        self.spinBox.valueChanged.connect(self.load)

        # start
        self.pushButton_4.clicked.connect(self.start)

        # download
        self.pushButton.clicked.connect(self.download)

        # bookmark
        self.pushButton_3.clicked.connect(self.setBookmark)
        self.comboBox.currentTextChanged.connect(self.changeBookmark)

        # close
        self.pushButton_2.clicked.connect(MainWindow.close)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def changechapterNumber(self):
        global nowPage
        if(nowPage == 1):
            self.load()
        else:
            self.spinBox.setValue(1)

    def start(self):
        global nowPage
        global nowChapter
        global chapterNumber
        global pageNumber
        global Directory
        global Bookmark

        nowChapter = self.spinBox_2.value()
        nowPage = self.spinBox.value()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            # ?????????????????????????????????????????????
            data = s.recv(1024).decode()
            Directory = ast.literal_eval(data)  # ??????????????????
            chapterNumber = len(Directory)
            pageNumber = Directory[nowChapter]
            self.spinBox_2.setRange(1, chapterNumber)
            self.spinBox.setRange(1, pageNumber)

            # ?????????????????????????????????????????????
            s.send(('XZYTXTREADER GET\r\nchapterNumber:' + str(nowChapter) + '\r\npageNumber:' + str(nowPage) + '\r\n').encode())
            page = s.recv(4096)
            page = page.decode('gb18030')
            self.textBrowser.clear()
            self.textBrowser.append(page)

        # ????????????????????????
        Bookmark = []
        fo = open("bookmark.txt", "r")
        list = fo.readlines()
        for fields in list:
            chapter = fields.split(" ")[0]
            page = fields.split(" ")[1].split("\n")[0]
            chapter = int(chapter)
            page = int(page)
            if chapter in range(1, chapterNumber + 1) and page in range(1, Directory[chapter] + 1):
                if (chapter, page) not in Bookmark:
                    Bookmark.append((chapter, page))
        fo.close()
        self.comboBox.clear()
        self.comboBox.addItem("")
        for (a, b) in Bookmark:
            self.comboBox.addItem("???" + str(a) + "?????????" + str(b) + "???")

    def load(self):
        global nowPage
        global nowChapter
        global chapterNumber
        global pageNumber
        global Directory

        nowChapter = self.spinBox_2.value()
        nowPage = self.spinBox.value()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            # ????????????????????????????????????????????????
            data = s.recv(1024).decode()
            pageNumber = Directory[nowChapter]
            self.spinBox.setRange(1, pageNumber)

            # ?????????????????????????????????????????????
            s.send(('XZYTXTREADER GET\r\nchapterNumber:' + str(nowChapter) + '\r\npageNumber:' + str(nowPage) + '\r\n').encode())
            page = s.recv(4096)
            page = page.decode('gb18030')
            self.textBrowser.clear()
            self.textBrowser.append(page)

    # ????????????
    def setBookmark(self):
        global nowPage
        global nowChapter
        global Bookmark

        if (nowChapter, nowPage) not in Bookmark:
            Bookmark.append((nowChapter, nowPage))
            self.comboBox.addItem("???" + str(nowChapter) + "?????????" + str(nowPage) + "???")
            fo = open("bookmark.txt", "a+")
            fo.write(str(nowChapter) + " " + str(nowPage)+"\n")
            fo.close()

    # ????????????
    def changeBookmark(self):
        global Bookmark

        if self.comboBox.currentIndex() >= 1:
            self.spinBox_2.setValue(Bookmark[self.comboBox.currentIndex() - 1][0])
            self.spinBox.setValue(Bookmark[self.comboBox.currentIndex() - 1][1])

    # ??????
    def download(self):
        global nowPage
        global nowChapter

        nowChapter = self.spinBox_2.value()
        nowPage = self.spinBox.value()

        # ????????????
        fileName = QtWidgets.QFileDialog.getExistingDirectory(None, "???????????????", "./")
        if(fileName == ""):
            return

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            data = s.recv(1024).decode()
            s.send(('XZYTXTREADER GET\r\nchapterNumber:' + str(nowChapter) + '\r\npageNumber:' + str(nowPage) + '\r\n').encode())

            # ????????????
            page = s.recv(4096)
            page = page.decode('gb18030')
            fo = open(fileName + "/" + "???" + str(nowChapter) + "??????" + str(nowPage) + "???" + ".txt", "w+")
            fo.write(page)
            fo.close()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "??????"))
        self.label_2.setText(_translate("MainWindow", "??????"))
        self.pushButton.setText(_translate("MainWindow", "??????"))
        self.pushButton_2.setText(_translate("MainWindow", "??????"))
        self.pushButton_3.setText(_translate("MainWindow", "????????????"))
        self.label_3.setText(_translate("MainWindow", "??????"))
        self.pushButton_4.setText(_translate("MainWindow", "????????????"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.setWindowTitle("???????????????by?????????")     # ??????????????????
    mainWindow.show()
    sys.exit(app.exec_())