 
#### About window
'''
    Copyright (C) 2020 Oliver Rodriguez
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
#### @author oliverrdz
#### https://oliverrdz.xyz

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_About(object):
    def setupUi(self, About):
        About.setObjectName("About")
        About.setEnabled(True)
        About.resize(562, 316)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("logo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        About.setWindowIcon(icon)
        self.label = QtWidgets.QLabel(About)
        self.label.setGeometry(QtCore.QRect(20, 20, 271, 271))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(About)
        self.label_2.setGeometry(QtCore.QRect(350, 50, 161, 31))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(About)
        self.label_3.setGeometry(QtCore.QRect(300, 110, 241, 61))
        self.label_3.setScaledContents(False)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.line = QtWidgets.QFrame(About)
        self.line.setGeometry(QtCore.QRect(330, 80, 191, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_4 = QtWidgets.QLabel(About)
        self.label_4.setGeometry(QtCore.QRect(380, 100, 64, 17))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(About)
        self.label_5.setGeometry(QtCore.QRect(330, 230, 191, 17))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(About)
        self.label_6.setGeometry(QtCore.QRect(340, 170, 161, 17))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(About)
        self.label_7.setGeometry(QtCore.QRect(300, 200, 241, 17))
        self.label_7.setObjectName("label_7")

        self.retranslateUi(About)
        QtCore.QMetaObject.connectSlotsByName(About)

    def retranslateUi(self, About):
        _translate = QtCore.QCoreApplication.translate
        About.setWindowTitle(_translate("About", "About SP"))
        self.label.setText(_translate("About", "<html><head/><body><p><img src=logo.svg></p></body></html>"))
        self.label_2.setText(_translate("About", "Soft Potato"))
        self.label_3.setText(_translate("About", "Free and open source electrochemical simulator"))
        self.label_4.setText(_translate("About", "v1.0.0"))
        self.label_5.setText(_translate("About", "<html><head/><body><p>Visit <a href=\"https://oliverrdz.xyz/?page_id=143\"><span style=\" text-decoration: underline; color:#0000ff;\">https://oliverrdxz.xyz</span></a></p></body></html>"))
        self.label_6.setText(_translate("About", "Licensed under GPL v3"))
        self.label_7.setText(_translate("About", "Copyright © 2020 Oliver Rodríguez"))
        self.label_5.setOpenExternalLinks(True)

