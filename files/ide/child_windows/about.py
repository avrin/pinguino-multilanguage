#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

from PySide import QtGui, QtCore

from ...frames.about import Ui_About

########################################################################
class About(QtGui.QDialog):

    def __init__(self):
        super(About, self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint |
                            QtCore.Qt.WindowSystemMenuHint |
                            QtCore.Qt.WindowStaysOnTopHint)

        self.about = Ui_About()
        self.about.setupUi(self)

        self.setWindowTitle(os.getenv("NAME")+" - "+self.windowTitle())

        self.about.label_name.setText(os.getenv("NAME")+" "+os.getenv("VERSION")+"."+os.getenv("SUBVERSION"))


        self.about.label.setPixmap(QtGui.QPixmap(":/logo/art/pinguino11.svg"))


        self.connect(self.about.pushButton_credits, QtCore.SIGNAL("clicked()"), lambda :self.about.stackedWidget.setCurrentIndex(1))
        self.connect(self.about.pushButton_license, QtCore.SIGNAL("clicked()"), lambda :self.about.stackedWidget.setCurrentIndex(2))
        self.connect(self.about.pushButton_about, QtCore.SIGNAL("clicked()"), lambda :self.about.stackedWidget.setCurrentIndex(0))
        self.connect(self.about.pushButton_close, QtCore.SIGNAL("clicked()"), self.close)
        self.connect(self.about.pushButton_close_2, QtCore.SIGNAL("clicked()"), self.close)
        self.connect(self.about.pushButton_close_3, QtCore.SIGNAL("clicked()"), self.close)

        self.about.stackedWidget.setCurrentIndex(0)
        self.about.tabWidget.setCurrentIndex(0)

        self.setStyleSheet("""
        font-family: ubuntu regular;
        font-weight: normal;

        """)

        self.center_on_screen()

    #----------------------------------------------------------------------
    def center_on_screen(self):

        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)