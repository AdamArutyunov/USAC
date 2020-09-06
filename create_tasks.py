import sys
import fb
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidgetItem, QVBoxLayout, QWidget

class App(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: white;")
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.picked_color = None

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(430, 130, 301, 371))
        self.tableWidget.setStyleSheet("background-color: white;")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)

        self.d_input_widget = QWidget(self.centralwidget)
        self.d_input_widget.setGeometry(70, 130, 211, 400)
        
        self.d_input_layout = QVBoxLayout(self.d_input_widget)

        self.d_input = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.d_input.setGeometry(QtCore.QRect(70, 110, 211, 26))
        self.d_input.setStyleSheet("background-color: white;")
        self.d_input.setObjectName("d_input")
        self.d_input.textChanged.connect(lambda: self.check_detail_exists(self.d_input.toPlainText()))

        self.detail_pushinfo = QtWidgets.QLabel(self.d_input_widget)
        self.detail_pushinfo.setGeometry(0, 0, 211, 60)
        self.detail_pushinfo.setFixedHeight(30)

        self.detail_scheme = QtWidgets.QLabel(self.d_input_widget)
        self.detail_scheme.setGeometry(0, 0, 211, 120)

        self.color_picker = QWidget(self.d_input_widget)
        self.red_button = QtWidgets.QPushButton(self.color_picker)
        self.white_button = QtWidgets.QPushButton(self.color_picker)
        self.black_button = QtWidgets.QPushButton(self.color_picker)

        self.red_button.setText('Красный')
        self.white_button.setText('Белый')
        self.black_button.setText('Чёрный')

        self.red_button.clicked.connect(lambda: self.change_picked_color('Красный'))
        self.white_button.clicked.connect(lambda: self.change_picked_color('Белый'))
        self.black_button.clicked.connect(lambda: self.change_picked_color('Чёрный'))
        
        self.butt_layout = QVBoxLayout(self.color_picker)
        self.butt_layout.addWidget(self.red_button)
        self.butt_layout.addWidget(self.white_button)
        self.butt_layout.addWidget(self.black_button)


        self.d_input_layout.addWidget(self.detail_pushinfo)
        self.d_input_layout.addWidget(self.detail_scheme)
        self.d_input_layout.addWidget(self.color_picker)


        self.appname = QtWidgets.QLabel(self.centralwidget)
        self.appname.setGeometry(QtCore.QRect(10, 40, 751, 41))
        self.appname.setStyleSheet("text-align: center;\n""")
        self.appname.setObjectName("appname")

        self.to_btn = QtWidgets.QPushButton(self.centralwidget)
        self.to_btn.setGeometry(QtCore.QRect(320, 270, 71, 31))
        self.to_btn.setStyleSheet("background-color: white;")
        self.to_btn.setEnabled(False)
        self.to_btn.setObjectName("to_btn")
        self.to_btn.clicked.connect(lambda: self.add_to_sl(find_by_param('id_num',
                                                                         self.d_input.toPlainText(),
                                                                         self.out), db))

        self.from_btn = QtWidgets.QPushButton(self.centralwidget)
        self.from_btn.setGeometry(QtCore.QRect(320, 310, 71, 31))
        self.from_btn.setStyleSheet("background-color: white;")
        self.from_btn.setEnabled(False)
        self.from_btn.setObjectName("from_btn")

        MainWindow.setCentralWidget(self.centralwidget)

        self.d_input_widget.hide()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        MainWindow.setWindowTitle(_translate("MainWindow", "Сменное задание"))

        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Название"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Номер"))

        self.to_btn.setText(_translate("MainWindow", "->"))
        self.appname.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; color:#000000;\">Создание сменного задания</span></p></body></html>"))
        self.from_btn.setText(_translate("MainWindow", "<-"))

    def check_detail_exists(self, detail, out=None):
        if not out:
            out = self.out
        a = find_by_param('id_num', detail, out)
        if a:
            self.to_btn.setEnabled(True)
            self.detail_pushinfo.setText(f'Название: {a["name"]}')
            print(os.getcwd() + f'/imgs/{a["id_num"]}.jpg')
            img = QtGui.QImage()
            img.load(os.getcwd() + f'/imgs/{a["id_num"]}.jpg')
            img = img.scaled(211, 211, QtCore.Qt.KeepAspectRatio)
            pix = QtGui.QPixmap.fromImage(img)
            self.detail_scheme.setPixmap(pix)
            self.d_input_widget.show()
        else:
            self.to_btn.setEnabled(False)
            self.d_input_widget.hide()

    def add_to_sl(self, doc, db):
        doc['status'] = 'Не покрашено'
        doc['pallet'] = None
        doc['color'] = self.picked_color
        db.collection('today_details').document(doc['id_num']).set(doc)
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0,
                                 QTableWidgetItem(doc['name']))
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1,
                                 QTableWidgetItem(doc['id_num']))

    def change_picked_color(self, color):
        self.picked_color = color


def find_by_param(key, value, fromm):
    for f in fromm:
        if f[key] == value:
            return f
        
QCoreApplication.addLibraryPath('platforms')
app = QApplication(sys.argv)
window = QMainWindow()
db, appli, cert = fb.firebase_connection()

ui = App()
ui.addLibraryPath('platforms/')
ui.setupUi(window)
ui.out = fb.parse_results(db, 'all_details')

window.show()
sys.exit(app.exec_())
