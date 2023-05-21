import sys
from time import sleep
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
import pandas as pd
from matplotlib import pyplot as plt


class PlotThread(QThread):
    star_change_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.star_change_signal.connect(self.change_plt)
    def run(self):
        while True:
            print('...')
            sleep(1)
    def change_plt(self, file):
        print(file)
        cnt = pd.read_excel(file)
        plt.rcParams['axes.unicode_minus'] = False
       # plt.figure(figsize=(400, 300), dpi=150)
        plt.title("低碳钢拉伸曲线")
        plt.ylabel("F(KN)")
        plt.xlabel("ΔL/mm")
        vy = [i/1000 for i in cnt['LoadValue']]
        plt.plot(cnt['PositionValue'],vy)
        plt.show()


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.load_ui()
    def load_ui(self):
        self.ui = uic.loadUi(r'./edtp.ui')
        print(self.ui.__dict__)
        self.ui.setWindowIcon(QIcon(r'./sztu.ico'))
        #h获取控件
        self.btn_select_file = self.ui.pushButton
        self.edit_file = self.ui.lineEdit
        self.btn_change = self.ui.pushButton_2
        #绑定槽函数
        self.btn_select_file.clicked.connect(self.select_file)
        self.btn_change.clicked.connect(self.push_btn_change)
        #创建子线程
        self.p_thread = PlotThread()
        self.p_thread.start()

    def select_file(self):
        file_name, file_type = QFileDialog.getOpenFileName(self, "选择Excel文件", './', "Excel Files (*.xls *.xlsx)")
        self.edit_file.setText(file_name)
    def push_btn_change(self):
        self.p_thread.star_change_signal.emit(self.edit_file.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.ui.show()
    app.exec()

