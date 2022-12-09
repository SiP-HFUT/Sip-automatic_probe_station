import serial#导入串口通信库
from time import sleep

ser = serial.Serial()

start='80 03 72 00 71'            #开关
data1='80 06 70 00 01 00 00 77'   #0.1
data2='80 06 70 00 1E 00 00 68'   #3.0
data3='80 06 70 00 64 00 00 12'   #1.0

sendstart=bytes.fromhex(start)
senddata1=bytes.fromhex(data1)
senddata2=bytes.fromhex(data2)
senddata3=bytes.fromhex(data3)


def port_open_recv():#对串口的参数进行配置
    ser.port='com3'
    ser.baudrate=9600
    ser.bytesize=8
    ser.stopbits=1
    ser.parity="N"#奇偶校验位
    ser.open()
    if(ser.isOpen()):
        print("串口打开成功！")
        ser.write(senddata1)        #初始化 0.1dBm
        ser.write(sendstart)
    else:
        print("串口打开失败！")
#isOpen()函数来查看串口的开闭状态



def port_close():
    ser.close()
    if(ser.isOpen()):
        print("串口关闭失败！")
    else:
        print("串口关闭成功！")
def send(send_data):
    if(ser.isOpen()):
        ser.write(send_data.encode('utf-8'))#编码
        print("发送成功",send_data)
    else:
        print("发送失败！")

if __name__ == '__main__':
    port_open_recv()
    while True:
        a=input("输入要发送的数据：")
        senddataa = bytes.fromhex(a)
        ser.write(senddataa)
        sleep(0.5)#起到一个延时的效果，这里如果不加上一个while True，程序执行一次就自动跳出了
