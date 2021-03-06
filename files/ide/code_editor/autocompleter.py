#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pickle
import os

from PySide.QtGui import QListWidget, QListWidgetItem
from PySide import QtCore, QtGui

from .autocomplete_icons import CompleteIcons
#from ..methods import constants as Constants

class PinguinoAutoCompleter(QListWidget):

    #----------------------------------------------------------------------
    def __init__(self):
        super(PinguinoAutoCompleter, self).__init__(None)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowSystemMenuHint |
                            QtCore.Qt.WindowStaysOnTopHint)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        self.setIconSize(QtCore.QSize(14, 14))
        self.set_height(300)

        self.setSpell(2)
        self.setEnabled(True)
        self.itemsList = []
        self.itemsListName = []
        self.temporal = {"variables" : [],
                         "functions" : [],
                         "directives" : [],
                         "arch8" : [],
                         "arch32" : [],
                         }


        self.namespaces = pickle.load(open(os.path.join(os.getenv("PINGUINO_USER_PATH"), "reserved.pickle"), "r"))

        icons = CompleteIcons()
        self.addItemsCompleter(self.namespaces["all"], icons.iconLibrary)
        del icons

        self.setStyleSheet("""
        font-family: ubuntu regular;
        font-weight: normal;

        """)


    #----------------------------------------------------------------------
    def set_arch_autocompleter(self):

        arch = os.getenv("PINGUINO_BOARD_ARCH")

        icons = CompleteIcons()

        if arch == "8":
            for item in self.namespaces["arch8"]:
                self.addTemporalItem("arch8", item, icons.iconLibrary)
            self.removeTemporalItems("arch32")

        elif arch == "32":
            for item in self.namespaces["arch32"]:
                self.addTemporalItem("arch32", item, icons.iconLibrary)
            self.removeTemporalItems("arch8")

        del icons

    #----------------------------------------------------------------------
    def hide(self, *args):
        super(PinguinoAutoCompleter, self).hide(*args)
        self.text_edit.setFocus()

    #----------------------------------------------------------------------
    def show(self, *args):
        self.set_arch_autocompleter()
        super(PinguinoAutoCompleter, self).show(*args)

    #----------------------------------------------------------------------
    def focusOutEvent(self, event):
        self.hide()
        QtGui.QListWidget.focusOutEvent(self, event)

    #----------------------------------------------------------------------
    def setEnabled(self, en):
        self.enabled = en

    #----------------------------------------------------------------------
    def set_height(self, visisble):
        self.resize(200, visisble)

    #----------------------------------------------------------------------
    def ajustWidth(self):
        hs = self.horizontalScrollBar()
        cont = 0
        while hs.isVisible() :
            self.resize(self.width()+5, self.height())
            cont += 1
            if cont > 100: return # :)

    #----------------------------------------------------------------------
    def ajustPos(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()

        cont = 0
        while self.pos().y() + size.height() - screen.height() > -10:
            self.move(self.pos().x(), self.pos().y() - 5)
            cont += 1
            if cont > 100: self.destroy()

        cont = 0
        while self.pos().x() + size.width() - screen.width() > -10:
            self.move(self.pos().x() - 5, self.pos().y())
            cont += 1
            if cont > 100: self.destroy()


    #----------------------------------------------------------------------
    def setSpell(self, int_):
        self.spell = int_

    #----------------------------------------------------------------------
    def down(self):
        current = self.currentRow()
        self.setCurrentRow(current+1)

    #----------------------------------------------------------------------
    def up(self):
        current = self.currentRow()
        self.setCurrentRow(current-1)

    #----------------------------------------------------------------------
    def addNewItem(self, name, icon=None):
        if not name in self.itemsListName:
            item = QListWidgetItem()
            if icon: item.setIcon(icon)
            item.setText(name)
            self.addItem(item)
            self.itemsList.append(item)
            self.itemsListName.append(name)
            return item

    #----------------------------------------------------------------------
    def addTemporalItem(self, llave, name, icon=None):
        item = self.addNewItem(name, icon)
        if item:
            self.temporal[llave].append(item)

    #----------------------------------------------------------------------
    def removeTemporalItems(self, llave):
        for item in self.temporal[llave]:
            index = self.getIndex(item.text())
            if index:
                self.itemsList.pop(index)
                #self.itemsList.remove(item)
                self.itemsListName.remove(item.text())
                self.takeItem(index)
        self.update()
        self.temporal[llave] = []

    #----------------------------------------------------------------------
    def getIndex(self, name, start=False):
        cont = 0
        for item in self.itemsList:
            if start:
                if item.text().lower().startswith(name.lower()): return cont
            else:
                if item.text() == name: return cont
            cont += 1
        return None

    #----------------------------------------------------------------------
    def addItemsCompleter(self, list_, icon=None):
        for text in list_:
            if not text in self.itemsListName:
                item = QListWidgetItem()
                if icon != None: item.setIcon(icon)
                item.setText(text)
                self.addItem(item)
                self.itemsList.append(item)
                self.itemsListName.append(item.text())

    #----------------------------------------------------------------------
    def popup(self, pos, index=None):

        ##hide autocompleter after 3s
        #hide_timer = QtCore.QTimer()
        #QtCore.QTimer.singleShot(3000, self.hide)
        #hide_timer.setSingleShot(True)
        #hide_timer.start()

        self.sortItems()
        self.itemsList.sort()

        if index == None:
            self.setCurrentRow(0)
            self.move(pos)
            self.show()
            self.setFocus()
            self.ajustWidth()
            self.ajustPos()
            return

        cont = self.getIndex(index, True)
        if not cont:
            self.hide()
            return

        if self.enabled:
            self.setCurrentRow(cont)
            item = cont + 5
            if item >= len(self.itemsList): item = -1
            self.scrollToItem(self.itemsList[item])

            self.move(pos)
            self.show()
            self.setFocus()

            self.ajustWidth()
            self.ajustPos()



