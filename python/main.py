
# -*- coding: utf-8 -*-
'''
Author: Liu Zheyuan
Copyright 2019 Liu Zheyuan, github/LeoAndGit>

'''

import sys
import time # 时间戳

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import qdarkstyle  # QSS样式表

from mainUI import Ui_Form #自动生成的界面
from deviceComScript import MySerial

import serial
import serial.tools.list_ports

class MyMainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):    
        super(MyMainWindow, self).__init__(parent)
        pg.setConfigOption('background', '#31363b')  # 设置背景为灰色
        pg.setConfigOption('foreground', 'w')  # 设置前景（包括坐标轴，线条，文本等等）为白色。
        #pg.setConfigOptions(antialias=True) # 使曲线看起来更光滑，而不是锯齿状

        self.ui = Ui_Form()
        self.ui.setupUi(self)
                
        ##创建线程实例
        self.thread1 = Thread1()

        self.thread1.sinOut1.connect(self.slotThread11)

    def linkSlot(self):
        self.thread1.link()

    def startSlot(self):
        self.thread1.setAndStart("start")

    def stopSlot(self):
        self.thread1.setAndStart("stop")

    def slotThread11(self, text): # 结果输出
        # self.ui.textEdit.setPlainText(text)
        # 格式化时间
        timeText = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.ui.textEdit.append(timeText + " : " + text)  # 自动添加回车


class Thread1(QtCore.QThread):
    sinOut1 = QtCore.pyqtSignal(str)

    def _init_(self,parent=None):
        super(Thread1,self).__init__(parent)

    def setAndStart(self, value):
        self.flag = value
        if value is not "stop":
            self.start()

    def link(self):
        """来自动连接在端口上的设备，会打开第一个串口
        注意：本方法可能无法跨平台使用，端口名相关部分未经确认
        一旦发现设备，将保持串口打开
        """
        self.serial = MySerial(
            port=None,
            baudrate=9600, # 串口波特率：9600bps
            # 莫名原因导致下述三项无法配置
            #bytesize=EIGHTBITS, # 8 位数据位
            #parity=PARITY_NONE, # 无校验位
            #stopbits=STOPBITS_ONE, # 1 位停止位
            timeout=0.2, # 读取超时0.2s
            xonxoff=False,
            rtscts=False,
            write_timeout=0.5, # 写超时0.5s
            dsrdtr=False,
            inter_byte_timeout=None,
            exclusive=None)
        if self.serial.is_open is True: #检测是否已经开启
            self.serial.close()
        # 获取串口列表
        self.plist = list(serial.tools.list_ports.comports())

        if len(self.plist) <= 0: # 无串口
            self.sinOut1.emit("no port")
        else:
            # 连接第一个串口
            plist_0 = list(self.plist[0])
            serialName = plist_0[0]
            self.serial.port = serialName
            self.serial.open()
            self.sinOut1.emit(serialName)
            self.serial.reset_input_buffer()

    def run(self):
        try:
            if self.flag is "start":
                self.serial.write(b"AT\r\n")
                answer = self.serial.read_until()
                # 后四个
                if answer[-4:] == b"OK\r\n":
                    self.sinOut1.emit("Success")
                else:
                    self.serial.reset_input_buffer() # 清空输入缓存
                    self.sinOut1.emit("Error")
        except serial.SerialException as e: # 串口操作出错
            self.sinOut1.emit(str(e))
           


if __name__=="__main__":  
    app = QtWidgets.QApplication(sys.argv)
    # 设置样式表
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    myWin = MyMainWindow()
    myWin.show()#向框架添加绘制事件
    sys.exit(app.exec_())