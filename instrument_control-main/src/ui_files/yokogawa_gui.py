# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yokogawa_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(965, 434)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.short_frame = QtWidgets.QFrame(self.centralwidget)
        self.short_frame.setGeometry(QtCore.QRect(150, 10, 391, 101))
        self.short_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.short_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.short_frame.setObjectName("short_frame")
        self.short_wavelength_label = QtWidgets.QLabel(self.short_frame)
        self.short_wavelength_label.setGeometry(QtCore.QRect(10, 0, 231, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.short_wavelength_label.setFont(font)
        self.short_wavelength_label.setObjectName("short_wavelength_label")
        self.short_start_label = QtWidgets.QLabel(self.short_frame)
        self.short_start_label.setGeometry(QtCore.QRect(0, 30, 41, 20))
        self.short_start_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.short_start_label.setObjectName("short_start_label")
        self.short_stop_label = QtWidgets.QLabel(self.short_frame)
        self.short_stop_label.setGeometry(QtCore.QRect(0, 60, 41, 20))
        self.short_stop_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.short_stop_label.setObjectName("short_stop_label")
        self.short_start_edit = QtWidgets.QLineEdit(self.short_frame)
        self.short_start_edit.setGeometry(QtCore.QRect(40, 30, 81, 20))
        self.short_start_edit.setObjectName("short_start_edit")
        self.short_stop_edit = QtWidgets.QLineEdit(self.short_frame)
        self.short_stop_edit.setGeometry(QtCore.QRect(40, 60, 81, 20))
        self.short_stop_edit.setObjectName("short_stop_edit")
        self.short_sensitivity_combobox = QtWidgets.QComboBox(self.short_frame)
        self.short_sensitivity_combobox.setGeometry(QtCore.QRect(290, 30, 91, 22))
        self.short_sensitivity_combobox.setObjectName("short_sensitivity_combobox")
        self.short_sensitivity_combobox.addItem("")
        self.short_sensitivity_combobox.addItem("")
        self.short_sensitivity_combobox.addItem("")
        self.short_sensitivity_combobox.addItem("")
        self.short_sensitivity_combobox.addItem("")
        self.short_sensitivity_combobox.addItem("")
        self.short_sensitivity_combobox.addItem("")
        self.short_sensitivity_label = QtWidgets.QLabel(self.short_frame)
        self.short_sensitivity_label.setGeometry(QtCore.QRect(220, 30, 61, 20))
        self.short_sensitivity_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.short_sensitivity_label.setObjectName("short_sensitivity_label")
        self.short_points_edit = QtWidgets.QLineEdit(self.short_frame)
        self.short_points_edit.setGeometry(QtCore.QRect(160, 30, 61, 20))
        self.short_points_edit.setObjectName("short_points_edit")
        self.short_points_label = QtWidgets.QLabel(self.short_frame)
        self.short_points_label.setGeometry(QtCore.QRect(120, 30, 41, 20))
        self.short_points_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.short_points_label.setObjectName("short_points_label")
        self.short_scantype_combobox = QtWidgets.QComboBox(self.short_frame)
        self.short_scantype_combobox.setGeometry(QtCore.QRect(290, 60, 91, 22))
        self.short_scantype_combobox.setObjectName("short_scantype_combobox")
        self.short_scantype_combobox.addItem("")
        self.short_scantype_combobox.addItem("")
        self.short_scantype_combobox.addItem("")
        self.short_scantype_label = QtWidgets.QLabel(self.short_frame)
        self.short_scantype_label.setGeometry(QtCore.QRect(220, 60, 61, 20))
        self.short_scantype_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.short_scantype_label.setObjectName("short_scantype_label")
        self.label = QtWidgets.QLabel(self.short_frame)
        self.label.setGeometry(QtCore.QRect(260, 0, 91, 16))
        self.label.setObjectName("label")
        self.connect_button = QtWidgets.QPushButton(self.centralwidget)
        self.connect_button.setGeometry(QtCore.QRect(37, 20, 75, 23))
        self.connect_button.setObjectName("connect_button")
        self.connections_edit = QtWidgets.QTextEdit(self.centralwidget)
        self.connections_edit.setGeometry(QtCore.QRect(20, 50, 111, 51))
        self.connections_edit.setObjectName("connections_edit")
        self.long_frame = QtWidgets.QFrame(self.centralwidget)
        self.long_frame.setGeometry(QtCore.QRect(560, 10, 391, 101))
        self.long_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.long_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.long_frame.setObjectName("long_frame")
        self.long_wavelength_label = QtWidgets.QLabel(self.long_frame)
        self.long_wavelength_label.setGeometry(QtCore.QRect(10, 0, 231, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.long_wavelength_label.setFont(font)
        self.long_wavelength_label.setObjectName("long_wavelength_label")
        self.long_sensitivity_combobox = QtWidgets.QComboBox(self.long_frame)
        self.long_sensitivity_combobox.setGeometry(QtCore.QRect(290, 30, 91, 22))
        self.long_sensitivity_combobox.setObjectName("long_sensitivity_combobox")
        self.long_sensitivity_combobox.addItem("")
        self.long_sensitivity_combobox.addItem("")
        self.long_sensitivity_combobox.addItem("")
        self.long_sensitivity_combobox.addItem("")
        self.long_sensitivity_combobox.addItem("")
        self.long_sensitivity_combobox.addItem("")
        self.long_sensitivity_combobox.addItem("")
        self.long_points_label = QtWidgets.QLabel(self.long_frame)
        self.long_points_label.setGeometry(QtCore.QRect(120, 30, 41, 20))
        self.long_points_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.long_points_label.setObjectName("long_points_label")
        self.long_scantype_label = QtWidgets.QLabel(self.long_frame)
        self.long_scantype_label.setGeometry(QtCore.QRect(220, 60, 61, 20))
        self.long_scantype_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.long_scantype_label.setObjectName("long_scantype_label")
        self.long_scantype_combobox = QtWidgets.QComboBox(self.long_frame)
        self.long_scantype_combobox.setGeometry(QtCore.QRect(290, 60, 91, 22))
        self.long_scantype_combobox.setObjectName("long_scantype_combobox")
        self.long_scantype_combobox.addItem("")
        self.long_scantype_combobox.addItem("")
        self.long_scantype_combobox.addItem("")
        self.long_stop_edit = QtWidgets.QLineEdit(self.long_frame)
        self.long_stop_edit.setGeometry(QtCore.QRect(40, 60, 81, 20))
        self.long_stop_edit.setObjectName("long_stop_edit")
        self.long_start_edit = QtWidgets.QLineEdit(self.long_frame)
        self.long_start_edit.setGeometry(QtCore.QRect(40, 30, 81, 20))
        self.long_start_edit.setObjectName("long_start_edit")
        self.long_start_label = QtWidgets.QLabel(self.long_frame)
        self.long_start_label.setGeometry(QtCore.QRect(0, 30, 41, 20))
        self.long_start_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.long_start_label.setObjectName("long_start_label")
        self.long_points_edit = QtWidgets.QLineEdit(self.long_frame)
        self.long_points_edit.setGeometry(QtCore.QRect(160, 30, 61, 20))
        self.long_points_edit.setObjectName("long_points_edit")
        self.long_stop_label = QtWidgets.QLabel(self.long_frame)
        self.long_stop_label.setGeometry(QtCore.QRect(0, 60, 41, 20))
        self.long_stop_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.long_stop_label.setObjectName("long_stop_label")
        self.long_sensitivity_label = QtWidgets.QLabel(self.long_frame)
        self.long_sensitivity_label.setGeometry(QtCore.QRect(220, 30, 61, 20))
        self.long_sensitivity_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.long_sensitivity_label.setObjectName("long_sensitivity_label")
        self.label_2 = QtWidgets.QLabel(self.long_frame)
        self.label_2.setGeometry(QtCore.QRect(250, 0, 91, 16))
        self.label_2.setObjectName("label_2")
        self.plot_glw = GraphicsLayoutWidget(self.centralwidget)
        self.plot_glw.setGeometry(QtCore.QRect(20, 160, 931, 231))
        self.plot_glw.setObjectName("plot_glw")
        self.scan_short_button = QtWidgets.QPushButton(self.centralwidget)
        self.scan_short_button.setGeometry(QtCore.QRect(590, 120, 75, 23))
        self.scan_short_button.setObjectName("scan_short_button")
        self.scan_long_button = QtWidgets.QPushButton(self.centralwidget)
        self.scan_long_button.setGeometry(QtCore.QRect(720, 120, 75, 23))
        self.scan_long_button.setObjectName("scan_long_button")
        self.scan_both_button = QtWidgets.QPushButton(self.centralwidget)
        self.scan_both_button.setGeometry(QtCore.QRect(850, 120, 75, 23))
        self.scan_both_button.setObjectName("scan_both_button")
        self.filelocation_edit = QtWidgets.QTextEdit(self.centralwidget)
        self.filelocation_edit.setGeometry(QtCore.QRect(30, 120, 431, 31))
        self.filelocation_edit.setObjectName("filelocation_edit")
        self.save_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.save_checkbox.setGeometry(QtCore.QRect(470, 126, 71, 21))
        self.save_checkbox.setChecked(True)
        self.save_checkbox.setObjectName("save_checkbox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 965, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Yokogawa OSA GUI"))
        self.short_wavelength_label.setText(_translate("MainWindow", "Short Wavelength Inputs (AQ6374)"))
        self.short_start_label.setText(_translate("MainWindow", "Start:"))
        self.short_stop_label.setText(_translate("MainWindow", "Stop:"))
        self.short_start_edit.setText(_translate("MainWindow", "1000"))
        self.short_stop_edit.setText(_translate("MainWindow", "1550"))
        self.short_sensitivity_combobox.setItemText(0, _translate("MainWindow", "Normal"))
        self.short_sensitivity_combobox.setItemText(1, _translate("MainWindow", "Normal Hold"))
        self.short_sensitivity_combobox.setItemText(2, _translate("MainWindow", "Normal Auto"))
        self.short_sensitivity_combobox.setItemText(3, _translate("MainWindow", "Mid"))
        self.short_sensitivity_combobox.setItemText(4, _translate("MainWindow", "High1"))
        self.short_sensitivity_combobox.setItemText(5, _translate("MainWindow", "High2"))
        self.short_sensitivity_combobox.setItemText(6, _translate("MainWindow", "High3"))
        self.short_sensitivity_label.setText(_translate("MainWindow", "Sensitivity:"))
        self.short_points_edit.setText(_translate("MainWindow", "8001"))
        self.short_points_label.setText(_translate("MainWindow", "Points:"))
        self.short_scantype_combobox.setItemText(0, _translate("MainWindow", "Single"))
        self.short_scantype_combobox.setItemText(1, _translate("MainWindow", "Repeat"))
        self.short_scantype_combobox.setItemText(2, _translate("MainWindow", "Stop"))
        self.short_scantype_label.setText(_translate("MainWindow", "Scan Type:"))
        self.label.setText(_translate("MainWindow", "350-1750nm"))
        self.connect_button.setText(_translate("MainWindow", "Connect"))
        self.long_wavelength_label.setText(_translate("MainWindow", "Long Wavelength Inputs (AQ6376)"))
        self.long_sensitivity_combobox.setItemText(0, _translate("MainWindow", "Normal"))
        self.long_sensitivity_combobox.setItemText(1, _translate("MainWindow", "Normal Hold"))
        self.long_sensitivity_combobox.setItemText(2, _translate("MainWindow", "Normal Auto"))
        self.long_sensitivity_combobox.setItemText(3, _translate("MainWindow", "Mid"))
        self.long_sensitivity_combobox.setItemText(4, _translate("MainWindow", "High1"))
        self.long_sensitivity_combobox.setItemText(5, _translate("MainWindow", "High2"))
        self.long_sensitivity_combobox.setItemText(6, _translate("MainWindow", "High3"))
        self.long_points_label.setText(_translate("MainWindow", "Points:"))
        self.long_scantype_label.setText(_translate("MainWindow", "Scan Type:"))
        self.long_scantype_combobox.setItemText(0, _translate("MainWindow", "Single"))
        self.long_scantype_combobox.setItemText(1, _translate("MainWindow", "Repeat"))
        self.long_scantype_combobox.setItemText(2, _translate("MainWindow", "Stop"))
        self.long_stop_edit.setText(_translate("MainWindow", "2000"))
        self.long_start_edit.setText(_translate("MainWindow", "1500"))
        self.long_start_label.setText(_translate("MainWindow", "Start:"))
        self.long_points_edit.setText(_translate("MainWindow", "8001"))
        self.long_stop_label.setText(_translate("MainWindow", "Stop:"))
        self.long_sensitivity_label.setText(_translate("MainWindow", "Sensitivity:"))
        self.label_2.setText(_translate("MainWindow", "1500-3400nm"))
        self.scan_short_button.setText(_translate("MainWindow", "Scan Short"))
        self.scan_long_button.setText(_translate("MainWindow", "Scan Long"))
        self.scan_both_button.setText(_translate("MainWindow", "Scan Both"))
        self.filelocation_edit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">C:\\Users\\Lynn\\Desktop\\instrument_control\\test.dat</p></body></html>"))
        self.save_checkbox.setText(_translate("MainWindow", "Save"))
from pyqtgraph import GraphicsLayoutWidget
