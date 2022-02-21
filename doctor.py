import smtplib

import pymysql
from PyQt5.QtWidgets import QMessageBox

from verefication import Ui_Verification
from TODO import Ui_TODO
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

global ui
global con
global Verification
global Ui_TODO
global TODOapp
global TODO
global myID
global pacient
global newDrugs
def send_email(message):
    sender = ""
    password = ""
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        # 1 - sender, 2 - recipient
        server.sendmail(sender, sender, message)

        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"
def enter():
    global ui
    global con
    global Verification
    global Ui_TODO
    global TODOui
    global TODOapp
    global TODO
    global myID
    newDrugs = []
    name = ui.textName.toPlainText().split()
    passw = ui.Pasword.toPlainText()
    if(len(name) != 3):
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setText("Неправильный логин или пароль")
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()
        return
    s = """SELECT person_id FROM doctor
                where lname = '{}' AND fname = '{}' AND patronymic = '{}' AND password = '{}';""".format(name[0],
                                                                                                         name[1],
                                                                                                         name[2], passw)

    print(s)
    cur = con.cursor()
    cur.execute(s)
    val = cur.fetchall()
    if (val == ()):
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setText("Неправильный логин или пароль")
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()
        return
    print("pass:{}".format(passw))
    myID = val[0]["person_id"]#TODO ззащиту от дурака
    if (len(val) == 1):
        print("{}--accepted".format(val))
        Verification.hide()
        TODOapp = QtWidgets.QApplication(sys.argv)
        TODO = QtWidgets.QMainWindow()
        TODOui = Ui_TODO()
        TODOui.setupUi(TODO)
        loadTODO()
        TODO.show()
    else:
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setText("Неправильный логин или пароль")
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()


from datetime import datetime


def loadTODO():
    global con
    global Ui_TODO
    global TODOui
    global TODOapp
    global TODO
    global myID
    global pacient
    TODOui.listTODO.itemClicked.connect(clickedItemPacient)
    pacient = dict()
    s = """SELECT p.fname, p.lname, HOUR(h.data) as H, MINUTE(h.data) as m , p.person_id as ID, h.id as idHis from history_of_diseases h INNER JOIN pacient p on h.pacient = p.person_id
where h.doctor ={} AND h.data > '{}'
ORDER BY h.data;""".format(myID, str(datetime.now())[:-7])
    cur = con.cursor()
    print(s)
    cur.execute(s)
    val = cur.fetchall()
    print(val)
    for i in val:
        TODOui.listTODO.addItem("{} {} {}:{}".format(i["lname"], i["fname"], i["H"], i["m"]))
        pacient["{} {} {}:{}".format(i["lname"], i["fname"], i["H"], i["m"])] = (i["ID"], i["idHis"])


global drugs
global pac, his
global nameIton
def clickedItemPacient(s):
    global con
    global Ui_TODO
    global TODOui
    global TODOapp
    global TODO
    global myID
    global pac, his
    global pacient
    global nameIton
    drugs = list()
    # Загрузка лекарств
    TODOui.listDrugs.clear()
    TODOui.deagnosesList.clear()
    pac, his = pacient[s.text()]
    s = """SELECT d.drug from drug d join history_of_diseases h
on d.id_diseases = h.id
where h.pacient = {};""".format(pac)
    cur = con.cursor()
    cur.execute(s)
    val = cur.fetchall()
    for i in val:
        TODOui.listDrugs.addItem(i["drug"])
    # Загрузка приемов

    TODOui.listHistory.clear()
    s = """SELECT dt.type, DATE(hd.data) as date from doctor_type dt
join history_of_diseases hd on hd.pacient = {}
where hd.doctor = dt.id;""".format(pac)
    cur = con.cursor()
    cur.execute(s)
    val = cur.fetchall()
    for i in val:
        TODOui.listHistory.addItem("{}:{}".format(i["type"], i["date"]))
    #грузка заигнозов (проблем)
    s = """
SELECT name from problem
where id_pacient = {};""".format(pac)
    cur = con.cursor()
    cur.execute(s)
    val = cur.fetchall()
    for i in val:
        TODOui.deagnosesList.addItem("{}".format(i["name"]))
    TODOui.senderDrugs.clicked.connect(adderDrugs)
    TODOui.sender.clicked.connect(sender)
def adderDrugs():
    global con
    global TODOui
    global  pac, his
    new = TODOui.textNewDrugs.text()
    TODOui.newDrugs.addItem(new)
    TODOui.textNewDrugs.clear()
    ## отправка на сервер
    s = "insert into drug values (NULL, '{}', {});".format(new, his)
    cur = con.cursor()
    cur.execute(s)
    con.commit()




def sender():
    global con
    global TODOui
    global pac, his
    test = TODOui.textAbout.toPlainText()
    problem = TODOui.newDiagnoses.text()
    s = "insert into problem values (NULL, {}, {}, '{}');".format(pac, his, problem)
    cur = con.cursor()
    cur.execute(s)

    s = "update history_of_diseases Set diagnosis = '{}' where id = {};".format( test, his )
    send_email("{}:{}\n{}".format(pac,problem, test ))
    cur.execute(s)
    con.commit()
    TODOui.textAbout.clear()
    TODOui.newDiagnoses.clear()
    TODOui.newDrugs.clear()
    TODOui.deagnosesList.clear()







con = pymysql.connect(host='84.23.54.19', user='admin', password='', database='hospital',
                      charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
app = QtWidgets.QApplication(sys.argv)
Verification = QtWidgets.QMainWindow()
ui = Ui_Verification()
ui.setupUi(Verification)
ui.pushButton.clicked.connect(enter)
Verification.show()
sys.exit(app.exec_())
