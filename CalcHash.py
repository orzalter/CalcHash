# coding:utf8
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from hash_ui import Ui_Form
from calc_md5 import CalcMd5
from threading import Thread
import time
import resource_rc


class MyWindows(Ui_Form, QMainWindow):
    def __init__(self):
        super(MyWindows, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Hash - v0.1.0 - orzalter')
        self.setWindowIcon(QIcon(':/ico.png'))
        self.progressBar_1.setProperty("value", 0)
        self.progressBar_2.setProperty("value", 0)
        self.timer = QBasicTimer()
        self.step = 0
        self.s_step = 0
        self.stop = 0
        self.calc = CalcMd5()

        # 信号与槽
        self.pushButton_1.clicked.connect(self.click_file)
        self.pushButton_2.clicked.connect(self.click_dir)
        self.pushButton_3.clicked.connect(self.click_clear)
        self.pushButton_4.clicked.connect(self.click_save)
        self.pushButton_5.clicked.connect(self.click_stop)

    def click_file(self):
        try:
            file_names = QFileDialog.getOpenFileNames(self, '选择文件')
            if file_names[0]:
                self.calc_hash(file_names[0])
        except Exception as e:
            pass

    def click_dir(self):
        try:
            dir_name = QFileDialog.getExistingDirectory(self, '选择文件').replace("/", "\\")
            if dir_name:
                dir_list = []
                dir_list.append(dir_name)
                self.calc_hash(dir_list)
        except Exception as e:
            pass

    def click_clear(self):
        self.textBrowser_1.clear()
        self.calc.set_stop(1)
        self.timer.stop()
        self.step = 0
        self.s_step = 0
        self.progressBar_1.setValue(self.step)
        self.progressBar_2.setValue(self.step)

    def click_save(self):
        try:
            file_name = QFileDialog.getSaveFileName(self, '保存文件', 'MD5.txt', filter="*.txt")
            with open(file_name[0], 'w') as f:
                f.write(self.textBrowser_1.toPlainText())
        except Exception as e:
            pass

    def click_stop(self):
        self.stop = 1
        self.calc.set_stop(1)
        self.timer.stop()

    def tuple2text(self, value):
        name = "文件: " + str(value[0])
        size = "大小: " + str(value[1]) + " 字节"
        time = "修改时间: " + str(value[2])
        if not value[3]:
            MD5 = "MD5: 权限不足,无法计算"
        else:
            MD5 = "MD5: " + str(value[3]).upper()
        text = name + "\n" + size + "\n" + time + "\n" + MD5 + "\n"
        return text

    def calc_hash(self, value):
        self.step = 0
        self.s_step = 0
        self.stop = 0
        self.progressBar_1.setValue(self.s_step)
        self.progressBar_2.setValue(self.step)
        self.calc.set_stop(0)
        self.doAction()
        th = Thread(target=self.file_thread, args=(value,))
        th.start()

    def file_thread(self, value):
        for i in self.calc.calc_md5(value):
            if self.stop == 1:
                break
            text = self.tuple2text(i)
            self.textBrowser_1.append(text)
            time.sleep(0.5)

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.step = 0
            return
        self.s_step = self.calc.run_size / self.calc.s_size * 100
        self.step = self.calc.count / self.calc.total_size * 100
        self.progressBar_1.setValue(self.s_step)
        self.progressBar_2.setValue(self.step)

    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
        self.step = 0
        self.s_step = 0
        self.progressBar_1.setValue(self.s_step)
        self.progressBar_2.setValue(self.step)
        self.timer.start(100, self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    q = MyWindows()
    q.show()
    sys.exit(app.exec_())
