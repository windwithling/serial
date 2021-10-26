from PySide2.QtWidgets import QApplication,QTextBrowser
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile,Signal,QObject
from PySide2 import QtCore
from threading import Thread,Timer
from time import sleep
import serial
from serial.serialwin32 import Serial
from serial.tools import list_ports
from time import sleep
import datetime
import com

class MySignals(QObject):

    # 定义一种信号，两个参数 类型分别是： QTextBrowser 和 字符串
    # 调用 emit方法 发信号时，传入参数 必须是这里指定的 参数类型
    text_print = Signal(QTextBrowser,str)

    # 还可以定义其他种类的信号
    update_table = Signal(str)

global_ms = MySignals()
class start():
    def __init__(self):
        file = QFile("communication.ui")   #D:/python/venv/Qt/serial/ui/communication.ui
        print(FileExistsError)
        file.open(QFile.ReadOnly)
        file.close()
        self.ui = QUiLoader().load(file)#返回窗体对象

        self.receive_thread = None#接收线程
        self.baudrate = None
        self.now_port = 'COM1'
        self.connect_flag = 0
        self.button1_flag = 0
        self.close_flag = 0
        self.port = []
        self.name = []
        self.trans_data = []
        self.rec_data = []
        self.ser = 0

        self.ui.comboBox2.addItems(['9600','19200','38400','115200'])
        self.ui.comboBox2.clearEditText( )
        #self.ui.comboBox2.setAlignment(QtCore.Qt.AlignCenter)
        #self.ui.comboBox2.clear()

        self.ui.button1.clicked.connect(self.button_handle1)
        self.ui.button2.clicked.connect(self.button_handle2)
        self.ui.button3.clicked.connect(self.button_handle3)
        self.ui.button4.clicked.connect(self.button_handle4)
        self.ui.button5.clicked.connect(self.button_handle5)
        self.ui.comboBox1.currentIndexChanged.connect(self.box_handle1)
        self.ui.comboBox2.currentIndexChanged.connect(self.box_handle2)
        global_ms.text_print.connect(self.printToGui)

    def printToGui(self,fb,text):
        fb.append(str(text))
        fb.ensureCursorVisible()

    def Emit(self):
        def threadFunc():
            global_ms.text_print.emit(self.ui.textBrowser1, '输出内容')
        thread = Thread(target=threadFunc)
        thread.start()

    def button_handle1(self):#开关串口
        if self.button1_flag:
            self.ui.button1.setText('打开串口')
            self.button1_flag = 0
            self.connect_flag = 0
            self.ui.label.clear()
            thread = Thread(target = self.close)
            thread.start()
            self.ui.comboBox1.clear()
        else:
            self.ui.button1.setText('关闭串口')
            self.button1_flag = 1
            thread = Thread(target = self.connect)
            thread.start()

    def button_handle2(self):#发送数据
        self.trans_data = list(self.ui.TextEdit.toPlainText())
        thread = Thread(target = self.Trans_Data)
        thread.start()
        #print(trans_data)


    def button_handle3(self):#清除发送
        self.ui.TextEdit.clear()
        self.trans_data = []

    def button_handle4(self):#搜索串口
        self.ui.comboBox1.clear()
        self.Print_Used_Com()
        self.ui.comboBox1.addItems(self.port)

    def button_handle5(self):
        self.ui.textBrowser1.clear()


    def box_handle1(self):
        self.now_port = self.ui.comboBox1.currentText()


    def box_handle2(self):
        self.baudrate = self.ui.comboBox2.currentText()

    def connect(self):
        if self.port != []:
            self.ser=serial.Serial(self.now_port,self.baudrate,timeout=5)
            self.ser.bytesize = 8
            self.ser.stopbits = 1
            self.ser.parity = "N"
            print(self.ser.name)
            if self.ser.is_open:
                self.connect_flag = 1
                print(self.now_port,self.baudrate)
                self.ui.label.setText('成功连接')
                self.receive_thread = Thread(target = self.Rec_Data)
                self.receive_thread.start()
                return True
            else:
                self.ui.label.setText('连接失败')
                return False
        else:
            #self.ui.label.setText('未找到串口')
            return False

    def Rec_Data(self):
        while self.connect_flag:
            data = ''
            #data = data.encode('utf-8')
            n = self.ser.inWaiting()
            #print(n)
            if n:
                sleep(0.02)
                n = self.ser.inWaiting()
                data = self.ser.read(n)
            n = self.ser.inWaiting()
            if len(data)>0 and n==0:
                try:
                    rec_data = data.decode()
                    global_ms.text_print.emit(self.ui.textBrowser1,rec_data)
                    print(rec_data)
                except Exception as e:
                    print(e)
                    break
            else:
                continue

    def close(self):
        #ser.close()
        #ser=serial.Serial(now_port,baudrate,timeout=5)
        try:
            self.ser.close()
            self.connect_flag = 0
        except Exception as e:
            print(e)

    def Print_Used_Com(self):
        port_list = list(serial.tools.list_ports.comports())
        self.port = []
        self.name = []
        for num in port_list:
            self.port.append(num[0])
            #self.name.append(num[3])
        if self.port==[]:
            self.ui.label.setText('未找到串口')
        print(self.port)


    def Trans_Data(self):
        try:
            str = ''.join(self.trans_data)
            self.ser.write(str.encode())
        except Exception as e:
            print(e)

if __name__ == '__main__':
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    Start = start()
    Start.ui.show()
    app.exec_()
