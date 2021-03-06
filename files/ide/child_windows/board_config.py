#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

from ...frames.board_config import Ui_BoardConfig
from .board_config_advance import BoardConfigAdvance
from PySide import QtGui, QtCore


########################################################################
class BoardConfig(QtGui.QDialog):

    def __init__(self, parent):
        super(BoardConfig, self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint |
                            QtCore.Qt.WindowSystemMenuHint |
                            QtCore.Qt.WindowStaysOnTopHint)

        self.board_config = Ui_BoardConfig()
        self.board_config.setupUi(self)
        self.main = parent

        self.setWindowTitle(os.getenv("NAME")+" - "+self.windowTitle())

        self.build_devices_arch()
        self.load_config()

        self.connect(self.board_config.radioButton_mode_bootloader, QtCore.SIGNAL("clicked()"), self.update_mode)
        self.connect(self.board_config.radioButton_mode_icsp, QtCore.SIGNAL("clicked()"), self.update_mode)

        self.connect(self.board_config.radioButton_arch_8, QtCore.SIGNAL("clicked()"), self.update_mode)
        self.connect(self.board_config.radioButton_arch_32, QtCore.SIGNAL("clicked()"), self.update_mode)

        self.connect(self.board_config.pushButton_advance, QtCore.SIGNAL("clicked()"), self.advance)
        self.connect(self.board_config.pushButton_ok, QtCore.SIGNAL("clicked()"), self.accept_config)
        self.connect(self.board_config.pushButton_cancel, QtCore.SIGNAL("clicked()"), self.terminate_config)

        #self.connect(self.board_config.checkBox_heapsize, QtCore.SIGNAL("clicked()"), self.update_heapsize)
        #self.connect(self.board_config.checkBox_mips16, QtCore.SIGNAL("clicked()"), self.update_mips16)

        self.closeEvent = self.terminate_config

        all_groups = [self.board_config.groupBox_arch,
                      #self.board_config.groupBox_extra,
                      self.board_config.groupBox_mode,
                      self.board_config.groupBox_bootloader,
                      self.board_config.groupBox_devices_8,
                      self.board_config.groupBox_devices_32]

        for group in all_groups:
            group.setStyleSheet("""
            QGroupBox{
                font-family: ubuntu regular;
                font-weight: bold;
            }
            """)

        self.setStyleSheet("""
        font-family: ubuntu regular;
        font-weight: normal;

        """)

        self.init_groups()
        self.center_on_screen()


    #----------------------------------------------------------------------
    def terminate_config(self, event=None):

        self.main.configIDE.load_config()
        self.close_advance()
        self.close()


    #----------------------------------------------------------------------
    def update_mips16(self):
        self.main.configIDE.set("Board", "mips16", self.board_config.checkBox_mips16.isChecked())


    #----------------------------------------------------------------------
    def update_heapsize(self):
        self.main.configIDE.set("Board", "heapsize", self.board_config.checkBox_heapsize.isChecked())


    #----------------------------------------------------------------------
    def accept_config(self):

        self.save_config()
        self.main.configIDE.save_config()
        self.main.statusbar_ide(self.main.get_status_board())
        self.close_advance()
        self.close()


    #----------------------------------------------------------------------
    def load_config(self):

        self.main.configIDE.load_config()

        arch = self.main.configIDE.config("Board", "arch", 8)
        self.board_config.radioButton_arch_8.setChecked(arch == 8)
        self.board_config.radioButton_arch_32.setChecked(arch == 32)
        self.board_config.pushButton_advance.setVisible(arch == 32)

        mode = self.main.configIDE.config("Board", "mode", "bootloader")
        self.board_config.radioButton_mode_bootloader.setChecked(mode == "bootloader")
        self.board_config.radioButton_mode_icsp.setChecked(arch == "icsp")

        bootloader = self.main.configIDE.config("Board", "bootloader", "v1_v2")
        self.board_config.radioButton_bootloader_v1_v2.setChecked(bootloader == "v1_v2")
        self.board_config.radioButton_bootloader_v4.setChecked(bootloader == "v4")

        #mips16 = self.main.configIDE.config("Board", "mips16", True)
        #self.board_config.checkBox_mips16.setChecked(mips16)

        #heapsize = self.main.configIDE.config("Board", "heapsize", True)
        #self.board_config.checkBox_heapsize.setChecked(heapsize)

        #self.update_mode()
        self.update_mode()


    #----------------------------------------------------------------------
    def save_config(self):

        if self.board_config.radioButton_arch_8.isChecked(): arch = 8
        else: arch = 32
        self.main.configIDE.set("Board", "arch", arch)

        if self.board_config.radioButton_mode_bootloader.isChecked(): mode = "bootloader"
        else: mode = "icsp"
        self.main.configIDE.set("Board", "mode", mode)

        if self.board_config.radioButton_bootloader_v1_v2.isChecked(): bootloader = "v1_v2"
        else: bootloader = "v4"
        self.main.configIDE.set("Board", "bootloader", bootloader)

        name = self.main.configIDE.config("Board", "board_"+str(arch), None)
        self.main.configIDE.set("Board", "board", name)


    #----------------------------------------------------------------------
    def update_mode(self):

        mode_boot = self.board_config.radioButton_mode_bootloader.isChecked()
        arch_8 = self.board_config.radioButton_arch_8.isChecked()
        self.board_config.groupBox_bootloader.setVisible(mode_boot and arch_8)

        if not mode_boot:
            self.board_config.label_warning.setText(QtGui.QApplication.translate("Frame", "WARNING!! this mode can overwite the bootloader code."))
        else:
            self.board_config.label_warning.setText("")


    #----------------------------------------------------------------------
    def init_groups(self):

        arch_8 = self.board_config.radioButton_arch_8.isChecked()
        self.board_config.groupBox_devices_32.setVisible(not arch_8)
        self.board_config.groupBox_devices_8.setVisible(arch_8)


    #----------------------------------------------------------------------
    def set_board_name(self, name, arch):

        def dummy():
            self.main.configIDE.set("Board", "board_"+arch, name)
        return dummy


    #----------------------------------------------------------------------
    def build_devices_arch(self):

        #8bits
        name_checked = self.main.configIDE.config("Board", "board_8", "Pinguino 2550")
        arch_8 = filter(lambda board:board.arch==8, self.main.pinguinoAPI._boards_)
        arch_8.sort()

        count = 0
        side = 0  #left
        for board in arch_8:
            if arch_8.index(board) == (len(arch_8) / 2) + 1:
                count = 0
                side = 1  #rigth

            radio = QtGui.QRadioButton(self.board_config.groupBox_devices_8)
            self.board_config.gridLayout_device_8.addWidget(radio, count, side, 1, 1)
            radio.setText(board.name)
            radio.setToolTip(board.proc)
            if name_checked == board.name: radio.setChecked(True)
            self.connect(radio, QtCore.SIGNAL("clicked()"), self.set_board_name(board.name, "8"))
            count += 1


        #32bits
        name_checked = self.main.configIDE.config("Board", "board_32", "PIC32 Pinguino OTG")
        arch_32 = filter(lambda board:board.arch==32, self.main.pinguinoAPI._boards_)
        arch_32.sort()

        count = 0
        side = 0  #left
        for board in arch_32:
            if arch_32.index(board) == (len(arch_32) / 2) + 1:
                count = 0
                side = 1  #rigth

            radio = QtGui.QRadioButton(self.board_config.groupBox_devices_32)
            self.board_config.gridLayout_device_32.addWidget(radio, count, side, 1, 1)
            radio.setText(board.name)
            radio.setToolTip(board.proc)
            if name_checked == board.name: radio.setChecked(True)
            self.connect(radio, QtCore.SIGNAL("clicked()"), self.set_board_name(board.name, "32"))
            count += 1


    #----------------------------------------------------------------------
    def advance(self):

        self.frame_advance = BoardConfigAdvance(self.main, "BOARDNAME")
        self.frame_advance.show()

    #----------------------------------------------------------------------
    def close_advance(self):

        try: assert self.frame_advance
        except: return
        self.frame_advance.close()


    #----------------------------------------------------------------------
    def center_on_screen(self):

        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
