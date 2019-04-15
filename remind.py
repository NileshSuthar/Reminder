# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reminder.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import winsound
from PyQt5 import QtCore, QtGui, QtWidgets
from table import Ui_MainWindow 
import sqlite3 as sql
import _thread
import time
from datetime import datetime
from win10toast import ToastNotifier
import pyttsx3;
engine = pyttsx3.init();


toaster = ToastNotifier()  

waitList = []
flag = 0 
class Ui_Dialog(object):
    obj = None
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(605, 433)
        Dialog.setWindowIcon(QtGui.QIcon('clock.png'))
        self.timeEdit = QtWidgets.QTimeEdit(Dialog)
        self.timeEdit.setEnabled(True)
        self.timeEdit.setGeometry(QtCore.QRect(140, 270, 118, 22))
        self.timeEdit.setObjectName("timeEdit")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(60, 270, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(60, 70, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(60, 330, 57, 13))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 390, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.showTime)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 390, 125, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.button_clicked)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(168, 10, 191, 31))
        font = QtGui.QFont()
        font.setFamily("Palatino Linotype")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.calendarWidget = QtWidgets.QCalendarWidget(Dialog)
        self.calendarWidget.setGeometry(QtCore.QRect(140, 60, 331, 191))
        self.calendarWidget.setObjectName("calendarWidget")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit.setGeometry(QtCore.QRect(140, 320, 331, 41))
        self.plainTextEdit.setObjectName("plainTextEdit")
        date = self.calendarWidget.selectedDate()
        

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    
    def button_clicked(self):
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        MainWindow.exec_()
    def showTime(self):
        date = self.calendarWidget.selectedDate().toString("dd-MM-yyyy")
        time = self.timeEdit.time().toString()
        text = self.plainTextEdit.toPlainText()
        reminderDateTime =  datetime.strptime(date + " " + time[:5],"%d-%m-%Y %H:%M")
        currentDateTime = datetime.now()
        timeDifference = int((reminderDateTime - currentDateTime).total_seconds())  
        _thread.start_new_thread( showNot, (text,timeDifference ) )
        db = sql.connect('test.db')
        
        db.execute('insert into test  values (?,?,?)',(date,time,text))
        db.commit()
        cursor = db.execute('select * from test ')
        for row in cursor:
            print(row)
    
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Reminder"))
        self.label.setText(_translate("Dialog", "TIME"))
        self.label_2.setText(_translate("Dialog", "DATE"))
        self.label_3.setText(_translate("Dialog", "REMINDER"))
        self.pushButton.setText(_translate("Dialog", "Save"))
        self.pushButton_2.setText(_translate("Dialog", "Show Database"))
        self.label_4.setText(_translate("Dialog", "Reminder Application"))

def setNotificationsTime(event_loop) : 
    currDT = datetime.now()
    db = sql.connect('test.db')
    cursor = db.execute('select * from test ')
    timeList = []
    msgTimeDict = {}
    
    for row in cursor : 
        dt = datetime.strptime(row[0] + " " + row[1][:5],"%d-%m-%Y %H:%M")
        diff = int((dt-currDT).total_seconds())
        if diff < 0 : 
            continue
        timeList.append(diff)
        msgTimeDict[diff] = row[2]
    timeList.sort()
    _thread.start_new_thread( showNot, (msgTimeDict[timeList[0]],timeList[0] ) )
    for ind,x in enumerate(timeList) : 
        if ind == 0 : 
            continue
        _thread.start_new_thread( showNot, (msgTimeDict[x],x - timeList[ind-1] ) )

def showNot(msg,t) : 
    time.sleep(t)
    winsound.Beep(700, 1000)
    time.sleep(1.2)
    
    engine.say(msg);
    engine.runAndWait() ;
    toaster.show_toast("Reminder", msg, icon_path= "icon.png", duration=3)
   

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    try : 
        setNotificationsTime(1)
    except: 
        pass
    sys.exit(app.exec_())
    

