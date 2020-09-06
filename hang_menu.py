from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
import fb
import sys
import cv2
from AIModule import AIModule as ai
import NFC


class QtCapture(QtWidgets.QWidget):
    def __init__(self, *args):
        super(QtWidgets.QWidget, self).__init__()
        self.fps = 24
        self.cap = cv2.VideoCapture(*args)

        self.video_frame = QtWidgets.QLabel(ui.camera_capture)
        self.lay = QtWidgets.QHBoxLayout(ui.camera_capture)
        self.lay.addWidget(self.video_frame)
        self.setLayout(self.lay)

    def setFPS(self, fps):
        self.fps = fps

    def nextFrameSlot(self):
        ret, frame = self.cap.read()
        frame = cv2.resize(frame, (292, 219))
        # My webcam yields frames in BGR format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.detail_shot = frame
        img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.video_frame.setPixmap(pix)

    def start(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000./self.fps)

    def stop(self):
        self.timer.stop()

    def deleteLater(self):
        self.cap.release()
        super(QtWidgets.QWidget, self).deleteLater()


class App(object):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: white;\n""font-family: \"Courier New\";")
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(10, 30, 781, 51))
        self.title.setObjectName("title")
        
        self.nd_title = QtWidgets.QLabel(self.centralwidget)
        self.nd_title.setGeometry(QtCore.QRect(30, 120, 131, 21))
        self.nd_title.setStyleSheet("color: black;")
        self.nd_title.setObjectName("nd_title")
        
        self.n_detail = QtWidgets.QLabel(self.centralwidget)
        self.n_detail.setGeometry(QtCore.QRect(30, 160, 161, 16))
        self.n_detail.setStyleSheet("color: black;")
        self.n_detail.setObjectName("n_detail")
        
        self.detail_name = QtWidgets.QLabel(self.centralwidget)
        self.detail_name.setGeometry(QtCore.QRect(30, 290, 161, 41))
        self.detail_name.setStyleSheet("color: black;")
        self.detail_name.setObjectName("detail_name")
        
        self.nod_title = QtWidgets.QLabel(self.centralwidget)
        self.nod_title.setGeometry(QtCore.QRect(30, 250, 131, 21))
        self.nod_title.setStyleSheet("color: black;")
        self.nod_title.setObjectName("nod_title")
        
        self.hang_title = QtWidgets.QLabel(self.centralwidget)
        self.hang_title.setGeometry(QtCore.QRect(180, 100, 611, 21))
        self.hang_title.setStyleSheet("color: black;")
        self.hang_title.setObjectName("hang_title")
        
        self.scheme_title = QtWidgets.QLabel(self.centralwidget)
        self.scheme_title.setGeometry(QtCore.QRect(190, 170, 301, 21))
        self.scheme_title.setStyleSheet("color: black;")
        self.scheme_title.setObjectName("scheme_title")
        
        self.camera_title = QtWidgets.QLabel(self.centralwidget)
        self.camera_title.setGeometry(QtCore.QRect(490, 170, 301, 21))
        self.camera_title.setStyleSheet("color: black;")
        self.camera_title.setObjectName("camera_title")
        
        self.hanging_scheme = QtWidgets.QLabel(self.centralwidget)
        self.hanging_scheme.setGeometry(QtCore.QRect(190, 200, 292, 219))
        self.hanging_scheme.setObjectName("hanging_scheme")
        
        self.camera_capture = QtWidgets.QWidget(self.centralwidget)
        self.camera_capture.setGeometry(QtCore.QRect(500, 200, 292, 219))
        self.camera_capture.setObjectName("camera_capture")
        self.capture = None
        self.startCapture()
        self.camera_capture.setLayout(self.capture.lay)
        
        self.check_button = QtWidgets.QPushButton(self.centralwidget)
        self.check_button.setGeometry(QtCore.QRect(550, 520, 221, 51))
        self.check_button.setStyleSheet("font-size: 18px;\n""color: black;\n""border: 1px solid black")
        self.check_button.setObjectName("check_button")
        self.check_button.clicked.connect(self.check_hanging)
        
        self.time_label = QtWidgets.QLabel(self.centralwidget)
        self.time_label.setGeometry(QtCore.QRect(20, 380, 141, 21))
        self.time_label.setStyleSheet("color: black;")
        self.time_label.setObjectName("time_label")
        
        self.hang_timer = QtWidgets.QLabel(self.centralwidget)
        self.hang_timer.setGeometry(QtCore.QRect(190, 370, 111, 41))
        self.hang_timer.setStyleSheet("color: black;")
        self.hang_timer.setObjectName("hang_timer")
        self.hang_timer.time = 210
        
        self.warning_label = QtWidgets.QLabel(self.centralwidget)
        self.warning_label.setGeometry(QtCore.QRect(20, 450, 291, 51))
        self.warning_label.setStyleSheet("color: black;")
        self.warning_label.setObjectName("warning_label")
        
        self.warning_icon = QtWidgets.QLabel(self.centralwidget)
        self.warning_icon.setGeometry(QtCore.QRect(340, 450, 51, 51))
        self.warning_icon.setStyleSheet("color: black;")
        self.warning_icon.setObjectName("warning_icon")
        
        self.check_status = QtWidgets.QLabel(self.centralwidget)
        self.check_status.setGeometry(QtCore.QRect(550, 470, 221, 21))
        self.check_status.setObjectName("check_status")

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)
        
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        
        MainWindow.setWindowTitle(_translate("MainWindow", "Подвеска детали"))
        
        self.title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:26pt; color:#000000;\">Завеска детали</span></p></body></html>"))
        self.nd_title.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">№ детали</span></p></body></html>"))
        self.n_detail.setText(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.detail_name.setText(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.nod_title.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Название</span></p></body></html>"))
        self.hang_title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">ЗАВЕСКА</span></p></body></html>"))
        self.scheme_title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Схема завески</p></body></html>"))
        self.camera_title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Захват камеры</p></body></html>"))
        self.check_button.setText(_translate("MainWindow", "Проверить деталь"))
        self.time_label.setText(_translate("MainWindow", "Время на завеску:"))
        self.hang_timer.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:18pt;\">210</span></p></body></html>"))
        self.warning_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ff0000;\">Деталь не завешена!</span></p></body></html>"))
        self.warning_icon.setText(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))

    def clear_content(self):
        self.n_detail.setText('')
        self.detail_name.setText('')
        self.warning_label.hide()
        self.warning_icon.hide()
        self.hanging_scheme.clear()
        self.camera_capture.hide()
        self.hang_timer.hide()

    def new_task(self):
        self.clear_content()
        self.out = fb.parse_results(db, 'today_details')
        self.out = [a for a in self.out if a['status'] == 'Не покрашено']
        if not self.out:
            print('Сменное задание пустое.')
            return
        self.curr_task = self.out.pop(0)
        self.n_detail.setText(self.curr_task['id_num'])
        self.detail_name.setText(self.curr_task['name'])
        self.camera_capture.show()
        self.hang_timer.show()
        self.hang_timer.time = 210
        ##### REAL ID
        try:
            ai_checker.load_model(ai_checker.models_list()[0])
        except:
            pass

    def startCapture(self):
        if not self.capture:
            self.capture = QtCapture(camera_n)
            self.capture.setFPS(24)
            self.capture.setParent(self.camera_capture)
            self.capture.setWindowFlags(QtCore.Qt.Tool)
        self.capture.start()

    def endCapture(self):
        self.capture.deleteLater()
        self.capture = None

    def update_timer(self):
        self.hang_timer.time -= 1

        if self.hang_timer.time < 0:
            self.warning_label.show()
            self.warning_icon.show()

        _translate = QtCore.QCoreApplication.translate
        self.hang_timer.setText(_translate("MainWindow", f"<html><head/><body><p><span style=\" font-size:18pt;\">{self.hang_timer.time}</span></p></body></html>"))

    def check_hanging(self):
        if not self.out:
            self.new_task()
        detail_shot = self.capture.detail_shot
        ok, result = ai_checker.check(detail_shot)
        print(ok, result)
        if ok:
            pallet = NFC.pallet_accordance(pallet_checker.getUid())
            self.curr_task['status'] = 'На покраске'
            self.curr_task['pallet'] = pallet
            db.collection('today_details').document(self.curr_task['id_num']).set(self.curr_task)
            self.new_task()
        else:
            self.warning_label.show()
        
camera_n = 2


app = QApplication(sys.argv)
window = QMainWindow()

db, appli, cert = fb.firebase_connection()

ai_checker = ai.DetailChecker()
pallet_checker = NFC.NFCAnalyzer('/dev/ttyACM0', 9600)

ui = App()
ui.setupUi(window)

ui.out = fb.parse_results(db, 'today_details')
ui.new_task()

window.show()
sys.exit(app.exec_())
