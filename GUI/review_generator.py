# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'review_generator.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ReviewGenerator(object):
    def setupUi(self, ReviewGenerator):
        ReviewGenerator.setObjectName("ReviewGenerator")
        ReviewGenerator.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/Dubito/Desktop/1634396985874.jpeg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ReviewGenerator.setWindowIcon(icon)
        ReviewGenerator.setAccessibleName("")
        ReviewGenerator.setAccessibleDescription("")
        self.toolButton = QtWidgets.QToolButton(ReviewGenerator)
        self.toolButton.setGeometry(QtCore.QRect(630, 20, 150, 30))
        self.toolButton.setObjectName("toolButton")
        self.label = QtWidgets.QLabel(ReviewGenerator)
        self.label.setGeometry(QtCore.QRect(10, 20, 111, 30))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(ReviewGenerator)
        self.lineEdit.setGeometry(QtCore.QRect(130, 20, 480, 30))
        self.lineEdit.setStyleSheet("")
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(ReviewGenerator)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 111, 30))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(ReviewGenerator)
        self.lineEdit_2.setGeometry(QtCore.QRect(130, 60, 481, 30))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.toolButton_2 = QtWidgets.QToolButton(ReviewGenerator)
        self.toolButton_2.setGeometry(QtCore.QRect(630, 60, 150, 30))
        self.toolButton_2.setObjectName("toolButton_2")
        self.label_3 = QtWidgets.QLabel(ReviewGenerator)
        self.label_3.setGeometry(QtCore.QRect(10, 140, 111, 30))
        self.label_3.setObjectName("label_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(ReviewGenerator)
        self.lineEdit_3.setGeometry(QtCore.QRect(130, 140, 331, 30))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_4 = QtWidgets.QLabel(ReviewGenerator)
        self.label_4.setGeometry(QtCore.QRect(10, 180, 111, 30))
        self.label_4.setObjectName("label_4")
        self.lineEdit_4 = QtWidgets.QLineEdit(ReviewGenerator)
        self.lineEdit_4.setGeometry(QtCore.QRect(130, 180, 331, 30))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(ReviewGenerator)
        self.lineEdit_5.setGeometry(QtCore.QRect(130, 100, 331, 30))
        self.lineEdit_5.setText("")
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_5 = QtWidgets.QLabel(ReviewGenerator)
        self.label_5.setGeometry(QtCore.QRect(10, 100, 111, 30))
        self.label_5.setObjectName("label_5")
        self.toolButton_5 = QtWidgets.QToolButton(ReviewGenerator)
        self.toolButton_5.setGeometry(QtCore.QRect(570, 230, 130, 30))
        self.toolButton_5.setObjectName("toolButton_5")
        self.toolButton_3 = QtWidgets.QToolButton(ReviewGenerator)
        self.toolButton_3.setGeometry(QtCore.QRect(100, 230, 130, 30))
        self.toolButton_3.setStyleSheet("background-color: rgb(85, 170, 255);\n"
"color: rgb(255, 255, 255);\n"
"border: 0;")
        self.toolButton_3.setObjectName("toolButton_3")
        self.toolButton_4 = QtWidgets.QToolButton(ReviewGenerator)
        self.toolButton_4.setGeometry(QtCore.QRect(250, 230, 300, 30))
        self.toolButton_4.setObjectName("toolButton_4")
        self.textBrowser = QtWidgets.QTextBrowser(ReviewGenerator)
        self.textBrowser.setGeometry(QtCore.QRect(0, 280, 801, 321))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(ReviewGenerator)
        QtCore.QMetaObject.connectSlotsByName(ReviewGenerator)

    def retranslateUi(self, ReviewGenerator):
        _translate = QtCore.QCoreApplication.translate
        ReviewGenerator.setWindowTitle(_translate("ReviewGenerator", "文献综述一键生成器 - By: Dubito"))
        self.toolButton.setText(_translate("ReviewGenerator", "选择文件夹"))
        self.label.setText(_translate("ReviewGenerator", "PDF论文位置："))
        self.label_2.setText(_translate("ReviewGenerator", "生成综述位置："))
        self.toolButton_2.setText(_translate("ReviewGenerator", "选择文件夹"))
        self.label_3.setText(_translate("ReviewGenerator", "APP Key："))
        self.label_4.setText(_translate("ReviewGenerator", "APP Secret："))
        self.label_5.setText(_translate("ReviewGenerator", "综述文件名："))
        self.toolButton_5.setText(_translate("ReviewGenerator", "查看源码"))
        self.toolButton_3.setText(_translate("ReviewGenerator", "开始生成"))
        self.toolButton_4.setText(_translate("ReviewGenerator", "如何获取APP Key"))
