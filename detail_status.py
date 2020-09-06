import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QHBoxLayout, QPushButton, QHeaderView, QGridLayout, QLabel
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import pyqtSlot, QRect, QTimer
from PyQt5 import QtCore, QtGui
import fb

 
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Статус сменного задания'
        self.left = 0
        self.top = 0
        self.width = 1200
        self.height = 900
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("background-color: white;")

        self.table_upwid = QWidget(self)
        self.tableWidget = QTableWidget(self.table_upwid)
        self.layout = QHBoxLayout(self.table_upwid)
        
        self.layout.addWidget(self.tableWidget)
        self.table_upwid.resize(600, 600)

        self.button = QPushButton('Обновить', self)
        self.button.setToolTip('Обновить сменное задание')
        self.button.move(610, 10)
        self.button.clicked.connect(self.updateTable)

        self.label_ready = QLabel(self)
        self.label_painting = QLabel(self)
        self.label_painted = QLabel(self)

        self.label_ready.move(610, 100)
        self.label_painting.move(610, 150)
        self.label_painted.move(610, 200)

        self.updateTable()

        self.updateLabels()

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTable)
        self.timer.start(2000)

        self.show()

    def updateTable(self):
        self.out = fb.parse_results(db)
        self.updateLabels()

        height = len(self.out)
        width = 5
        
        self.tableWidget.setRowCount(height)
        self.tableWidget.setColumnCount(width)
        
        header = self.tableWidget.horizontalHeader()
        for i in range(width):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

        self.tableWidget.setHorizontalHeaderLabels(['Название', 'Номер', 'Статус', '№ палеты', 'Цвет'])
        my_keys = ['name', 'id_num', 'status', 'pallet', 'color']
        for i in range(height):
                for j in range(width):
                    self.tableWidget.setItem(i, j,
                                            QTableWidgetItem(str(self.out[i][my_keys[j]])))
                    self.tableWidget.item(i, j).setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableWidget.item(i, j).setBackground(QColor(*self.get_cell_color(self.tableWidget.item(i, j))))

    def get_cell_color(self, QTWI):
        QTWI = QTWI.text()
        if QTWI == 'На покраске':
            return 255, 128, 0
        if QTWI == 'Покрашено':
            return 0, 255, 0
        if QTWI == 'Не покрашено':
            return 255, 0, 0


        if QTWI == 'Красный':
            return 255, 0, 0
        if QTWI == 'Белый':
            return 255, 255, 255
        if QTWI == 'Чёрный':
            return 100, 100, 100
        return 255, 255, 255

    def counter(self, out):
        ready = 0
        painting = 0
        painted = 0
        for i in out:
            if i['status'] == 'Не покрашено':
                ready += 1
            elif i['status'] == 'На покраске':
                painting += 1
            elif i['status'] == 'Покрашено':
                painted += 1
        return painted, painting, ready

    def updateLabels(self):
        painted, painting, ready = self.counter(self.out)
        self.label_ready.setText('Не покрашено: ' + str(ready))
        self.label_painting.setText('На покраске: ' + str(painting))
        self.label_painted.setText('Покрашено: ' + str(painted))
            
        
def dtd():
    out = fb.parse_results(db)
    for o in out:
        db.collection('today_details').document(o['id_num']).delete()

db, app, cred = fb.firebase_connection()


app = QApplication(sys.argv)
ex = App()
ex.updateTable()

sys.exit(app.exec_())

