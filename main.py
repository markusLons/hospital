
from PyQt5 import QtCore, QtGui, QtWidgets
import pymysql
from PyQt5.QtWidgets import QMainWindow, QMessageBox
import smtplib

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 512)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.doctor = QtWidgets.QComboBox(self.centralwidget)
        self.doctor.setGeometry(QtCore.QRect(20, 100, 271, 31))
        self.doctor.setObjectName("doctor")
        self.pacient = QtWidgets.QComboBox(self.centralwidget)
        self.pacient.setGeometry(QtCore.QRect(20, 160, 271, 31))
        self.pacient.setObjectName("pacient")
        self.day = QtWidgets.QCalendarWidget(self.centralwidget)
        self.day.setGeometry(QtCore.QRect(20, 220, 271, 161))
        self.day.setObjectName("day")
        self.sender = QtWidgets.QPushButton(self.centralwidget)
        self.sender.setGeometry(QtCore.QRect(20, 450, 271, 31))
        self.sender.setObjectName("sender")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 80, 241, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 140, 281, 16))
        self.label_2.setObjectName("label_2")
        self.time = QtWidgets.QComboBox(self.centralwidget)
        self.time.setGeometry(QtCore.QRect(20, 410, 271, 31))
        self.time.setObjectName("time")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 390, 221, 16))
        self.label_3.setObjectName("label_3")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(310, 10, 321, 471))
        self.textEdit.setObjectName("textEdit")
        self.TypeBox = QtWidgets.QComboBox(self.centralwidget)
        self.TypeBox.setGeometry(QtCore.QRect(20, 42, 271, 31))
        self.TypeBox.setObjectName("TypeBox")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(40, 10, 251, 21))
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Запись клиента"))
        self.sender.setText(_translate("MainWindow", "Записать"))
        self.label.setText(_translate("MainWindow", "Доктор"))
        self.label_2.setText(_translate("MainWindow", "Пациент"))
        self.label_3.setText(_translate("MainWindow", "Время записи"))
        self.label_4.setText(_translate("MainWindow", "Направление"))
class MainWindow(QMainWindow, Ui_MainWindow):
    tupesDoctors =""
    def getNanesPacient(self,  con):
        cur = ""
        try:
            cur = con.cursor()
            cur.execute("SELECT * FROM pacient")
        except:
            self.con = pymysql.connect(host='84.23.54.19', user='admin', password='1610249MSMV2022NTO',
                                       database='hospital',
                                       charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
            cur.execute("SELECT * FROM pacient")
        rows = cur.fetchall()
        names = []
        for i in rows:
            names.append("{} {} {}".format(i["lname"], i["fname"], i["patronymic"]))
        print(names)
        return names

    def getNanesDoctor(self, con):

        cur = ""
        try:
            cur = con.cursor()
            cur.execute("SELECT * FROM doctor")
        except:
            self.con = pymysql.connect(host='84.23.54.19', user='admin', password='1610249MSMV2022NTO',
                                       database='hospital',
                                       charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
            cur = con.cursor()
            cur.execute("SELECT * FROM doctor")

        rows = cur.fetchall()
        names = []
        for i in rows:
            names.append("{} {} {}".format(i["lname"], i["fname"], i["patronymic"]))
        return names
    con = ""
    def getDoctorsInType(self):
        DT = self.TypeBox.currentText()
        print(DT)
        self.doctor.clear()
        cur = ""
        s = "SELECT lname, fname, patronymic from doctor where type ={};".format(self.tupesDoctors[DT])
        try:
            cur = self.con.cursor()
            cur.execute(s)
        except:
            self.con = pymysql.connect(host='84.23.54.19', user='admin', password='1610249MSMV2022NTO',
                                       database='hospital',
                                       charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
            cur = self.con.cursor()
            cur.execute(s)
        rows = cur.fetchall()
        for i in rows:
            self.doctor.addItem("{} {} {}".format(i["lname"], i["fname"],i["patronymic"] ))


        print(self.TypeBox.currentText())
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.day.clicked['QDate'].connect(self.show_date_func)
        self.sender.clicked.connect(self.sendInfo)
        self.con = pymysql.connect(host='84.23.54.19', user='admin', password='1610249MSMV2022NTO', database='hospital',
                                       charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        self.TypeBox.currentTextChanged.connect(self.getDoctorsInType)
        namesDoc = self.getNanesDoctor( self.con)
        namesPaci = self.getNanesPacient( self.con)
        for i in namesDoc:
            self.doctor.addItem(i)
        for i in namesPaci:
            self.pacient.addItem(i)
            print(i)
        self.getAllTypes()
    def getAllTypes(self):
        cur = self.con.cursor()
        cur.execute("SELECT * from doctor_type;")
        rows = cur.fetchall()
        self.tupesDoctors = dict()
        for i in rows:
            self.tupesDoctors[i["type"]] = i["id"]
            self.TypeBox.addItem(i["type"])



    def getFreeTimesOn(self):
        self.sender.setEnabled(True)
        self.time.clear()
        doctor = self.doctor.currentText().split()
        date = self.day.selectedDate()
        cur = ""
        try:
            cur = self.con.cursor()
            cur.execute("""select EXTRACT( HOUR FROM h.data) as hour,EXTRACT( MINUTE FROM h.data) as minute
                                    from history_of_diseases h INNER JOIN doctor d
                                    on h.doctor = d.person_id
                                    where d.fname = '{}' AND
                                          d.lname = '{}' AND
                                          d.patronymic = '{}' AND
                                          EXTRACT( DAY FROM h.data) = {} AND
                                          EXTRACT( MONTH FROM h.data) = {} AND
                                          EXTRACT( YEAR FROM h.data) = {};
                                    """.format(doctor[1], doctor[0], doctor[2], date.day(), date.month(), date.year()))

        except:

            self.con = pymysql.connect(host='84.23.54.19', user='admin', password='1610249MSMV2022NTO',
                                       database='hospital',
                                       charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
            cur = self.con.cursor()
            cur.execute("""select EXTRACT( HOUR FROM h.data) as hour,EXTRACT( MINUTE FROM h.data) as minute
                                               from history_of_diseases h INNER JOIN doctor d
                                               on h.doctor = d.person_id
                                               where d.fname = '{}' AND
                                                     d.lname = '{}' AND
                                                     d.patronymic = '{}' AND
                                                     EXTRACT( DAY FROM h.data) = {} AND
                                                     EXTRACT( MONTH FROM h.data) = {} AND
                                                     EXTRACT( YEAR FROM h.data) = {};
                                               """.format(doctor[1], doctor[0], doctor[2], date.day(), date.month(),
                                                          date.year()))

        rows = cur.fetchall()
        print(rows)
        timesOnDay = ["8:0", "8:10", "8:20", "8:30", "8:40", "8:50",
                      "9:0", "9:10", "9:20", "9:30", "9:40", "9:50",
                      "10:0", "10:10", "10:20", "10:30", "10:40", "10:50",
                      "11:0", "11:10", "11:20", "11:30", "11:40", "11:50",
                      "12:0", "12:10", "12:20", "12:30", "12:40", "12:50",
                      "13:0", "13:10", "13:20", "13:30", "13:40", "13:50",
                      "14:0", "14:10", "14:20", "14:30", "14:40", "14:50",
                      "15:0", "15:10", "15:20", "15:30", "15:40", "15:50",
                      "16:0", "16:10", "16:20", "16:30", "16:40", "16:50",
                      "17:0", "17:10", "17:20", "17:30", "17:40", "17:50",
                      "18:0", "18:10", "18:20", "18:30", "18:40", "18:50",
                      "19:0", "19:10", "19:20", "19:30", "19:40", "19:50",
                      "20:0", "20:10", "20:20", "20:30", "20:40", "20:50"]

        print(rows)
        try:
            for i in rows:
                timesOnDay.remove("{}:{}".format(int(i["hour"]), int(i["minute"])))
            for i in timesOnDay:
                self.time.addItem(i)
        except ValueError:
            self.sender.setEnabled(False)
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка записи")
            msg.setText("Нет времени для записи")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            return
    def show_date_func(self):
        self.getFreeTimesOn()
    def getIdPacientOnName(self, name):
        name = name.split()
        s = "SELECT person_id FROM pacient where fname = '{}' and lname = '{}' and patronymic ='{}';".format(name[1], name[0], name[2])
        try:
            cur = self.con.cursor()
            cur.execute(s)
        except:
            self.con = pymysql.connect(host='84.23.54.19', user='admin', password='1610249MSMV2022NTO',
                                       database='hospital',
                                       charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
            cur = self.con.cursor()
            cur.execute(s)

        s = cur.fetchall()
        print(int(s[0]["person_id"]))
        return int(s[0]["person_id"])
    def getIdDoctorOnName(self, name):
        name = name.split()
        s = "SELECT person_id FROM doctor where fname = '{}' and lname = '{}' and patronymic ='{}';".format(name[1], name[0], name[2])
        cur = self.con.cursor()
        cur.execute(s)
        s = cur.fetchall()
        return int(s[0]["person_id"])

    def sendInfo(self):
        text = self.textEdit.toPlainText()
        date = self.day.selectedDate()
        time = self.time.currentText()
        doctor = self.doctor.currentText()
        pacient = self.pacient.currentText()
        s = "INSERT INTO history_of_diseases VALUES (NULL, '{} {}' ,{},{}, '{}', {});".format(self.day.selectedDate().toString("yyyy-MM-dd"), time, self.getIdPacientOnName(pacient), self.getIdDoctorOnName(doctor), text, "NULL")
        print(text, date, time, doctor, pacient)
        cur = self.con.cursor()
        cur.execute(s)
        self.con.commit()
        self.getFreeTimesOn()





if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
