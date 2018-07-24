# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(751, 289)
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../home/kurozero/Pictures/YTDownloader_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.txt_yt = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_yt.setGeometry(QtCore.QRect(180, 30, 561, 30))
        self.txt_yt.setObjectName("txt_yt")
        self.cb_resolution = QtWidgets.QComboBox(self.centralwidget)
        self.cb_resolution.setGeometry(QtCore.QRect(180, 70, 86, 30))
        self.cb_resolution.setObjectName("cb_resolution")
        self.lbl_yt = QtWidgets.QLabel(self.centralwidget)
        self.lbl_yt.setGeometry(QtCore.QRect(10, 30, 161, 31))
        self.lbl_yt.setObjectName("lbl_yt")
        self.lbl_resolution = QtWidgets.QLabel(self.centralwidget)
        self.lbl_resolution.setGeometry(QtCore.QRect(10, 70, 121, 31))
        self.lbl_resolution.setObjectName("lbl_resolution")
        self.lbl_type = QtWidgets.QLabel(self.centralwidget)
        self.lbl_type.setGeometry(QtCore.QRect(10, 110, 111, 31))
        self.lbl_type.setObjectName("lbl_type")
        self.cb_type = QtWidgets.QComboBox(self.centralwidget)
        self.cb_type.setGeometry(QtCore.QRect(180, 110, 86, 30))
        self.cb_type.setObjectName("cb_type")
        self.cb_extension = QtWidgets.QComboBox(self.centralwidget)
        self.cb_extension.setGeometry(QtCore.QRect(180, 150, 86, 30))
        self.cb_extension.setObjectName("cb_extension")
        self.lbl_extension = QtWidgets.QLabel(self.centralwidget)
        self.lbl_extension.setGeometry(QtCore.QRect(10, 150, 111, 31))
        self.lbl_extension.setObjectName("lbl_extension")
        self.btn_download = QtWidgets.QPushButton(self.centralwidget)
        self.btn_download.setGeometry(QtCore.QRect(650, 200, 88, 30))
        self.btn_download.setObjectName("btn_download")
        self.btn_test = QtWidgets.QPushButton(self.centralwidget)
        self.btn_test.setGeometry(QtCore.QRect(550, 200, 88, 30))
        self.btn_test.setObjectName("btn_test")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 751, 27))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "YouTube Downloader"))
        self.lbl_yt.setText(_translate("MainWindow", "YouTube URL/Video ID"))
        self.lbl_resolution.setText(_translate("MainWindow", "Video resolution"))
        self.lbl_type.setText(_translate("MainWindow", "Download type"))
        self.lbl_extension.setText(_translate("MainWindow", "Video extension"))
        self.btn_download.setText(_translate("MainWindow", "Download"))
        self.btn_test.setText(_translate("MainWindow", "Test"))

