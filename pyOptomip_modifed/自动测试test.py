# -*- coding: utf-8 -*-
import time
import pyvisa as visa
import math

class CorvusEcoClass:
    def __init__(self, ser):
        self.ser = ser  # ser是serial，串口

    def connect(self, my_instrument):  # self,visaName,rm,速度,加速度,NumberOfAxis
        self.ser = my_instrument
        self.ser.baud_rate = 9600
        self.ser.read_termination = '\r'
        self.ser.write_termination = '\r'
        self.ser.write('*IDN?')  # 查询设备ID号
        print(self.ser.read_raw().decode())
        print("Connected\n")
        self.ser.write('AXIs 1~2')#选择坐标轴

        '''
        try:
            self.ser.write('%d setdim' % (NumberOfAxis)) #NumberOfAxis: {__ge__}) -> None
            if NumberOfAxis >= 1:
                self.ser.write('1 1 setaxis')
                print('Axis 1 Enabled.')
            if NumberOfAxis >= 2:
                self.ser.write('1 2 setaxis')
                print('Axis 2 Enabled.')
            else:
                self.ser.write('0 2 setaxis')#大于1小于2
            if NumberOfAxis >= 3:
                self.ser.write('1 3 setaxis')
                print('Axis 3 Enabled.')
            else:
                self.ser.write('0 3 setaxis')#大于2小于3
            self.NumberOfAxis = NumberOfAxis
        except:
            self.showErr()#小于1
        '''

        #设置单位为微米um
        #self.ser.write(':UNIT 2') #p123页
        #print('Units are set to: Microns(um)\n')

        #不设置加速度

        # set output port 不设置端口
        # self.ser.write('1 setout port=<port>') #其中<port>表示要设置的输出端口号


        # set trigger out 触发器 不确定ds102中有没有触发器这个功能

        #self.setcloop(1)

    def disconnect(self):
        self.ser.close()
        print('Corvus Eco Disconnected')

    # Units: (Unit/s) use setunit command 设置速度 SELSP 0~9
    def setVelocity(self, velocity):
        self.ser.write(':SELSP %d' % velocity)#百分号左右需要加其他空格，以确保不会被解释为其他字符
        #response = self.ser.read_raw().decode()  # 然后使用ser.read_raw()函数读取设备的响应，最后将响应解码并打印出来。
        #print("SELectSPeed set to: table " + response)

    #此处无加速度，无闭环控制，无模拟数字切换

    def setclperiod(self, direction, distance):#方向与距离，不确定这里需不需要定义哪个轴
        #原先方向是+和-，现在是0/1，
        try:
            self.ser.write('PULSe %d:GO %d' % (distance, direction))#GO是方向，pulse是各轴脉冲恒定量。
            print('Clperiod Set Successfully')
        except:
            self.showErr()

    #未定义setnselpos
    unit = ["pulse","um","mm"]
    units = unit[0]

    def setunit(self, unit):
        self.ser.write('AXI1:UNIT %d' % (unit))
        self.ser.write('AXI2:UNIT %d' % (unit))
        print('Units set successfully.')

    def getunit(self, AXI):#输入getunit（1）获取x轴单位
        self.ser.write('AXI%d:unit?' % AXI)
        get = self.ser.read()
        print ('AXI %d is setted to  ' % AXI + get)

        # response = int(self.ser.read_raw().decode().replace('\r', ''))
        # self.units = self.unit[response]
        # print('Axis %d is set to unitvalue: %s' % (AXI, self.units))

    # =======Movement functions============
    def moveX(self, distance):
        #轴指定指令：参数设定指令：驱动指令
        try:
            if distance > 0:
                self.ser.write('AXI1:PULSe %d:GO 0' % distance)
            if distance < 0:
                distance = -distance
                self.ser.write('AXI1:PULSe %d:GO 1' % distance)
        except:
            print('An Error has occured')
            self.showErr()

    def moveY(self,distance):
        try:
            if distance > 0:
                self.ser.write('AXI2:PULSe %d:GO 0' % distance)
            if distance < 0:
                distance = -distance
                self.ser.write('AXI2:PULSe %d:GO 1' % distance)
        except:
            print('An Error has occured')
            self.showErr()

    #同时移动多个轴
    def moveRelative(self, x, y=0, z=0):
        try:
            if x > 0:
                self.ser.write('AXI1:PULSe %.6f:GO 1' % x)   # %轴：参数：轴：参数
            if x < 0:
                x = -x
                self.ser.write('AXI1:PULSe %.6f:GO 0' % x)
            if y > 0:
                self.ser.write('AXI2:PULSe %.6f:GO 0' % y)
            if y < 0:
                y = -y
                self.ser.write('AXI2:PULSe %.6f:GO 1' % y)
        except:
            print('An Error has occured')
            self.showErr()
        self.waitMoveComplete()

    def moveAbsoluteXY(self, x, y):#绝对位置移动
        self.ser.write('AXI1:GOABS %d' % -x)
        self.ser.write('AXI2:GOABS %d' % y)

    def waitMoveComplete(self):
        while int(self.ser.query('MOTION')) & 1:
            time.sleep(0.001)

    def getPosition(self):
        '''
        self.ser.write("AXI1:POS?")
        x = self.ser.read_raw().decode()
        self.ser.write("AXI2:POS?")
        y = self.ser.read_raw().decode()
        print('坐标:%s %s' % (x.replace('\r', ''),y.replace('\r', '')) )
        '''
        try:
            self.ser.write("AXI1:POS?")  # AXI1~2:POS?
            x = self.ser.read()
            x = int(x)
            print ('x is %d' % x)
            print (x)

            self.ser.write("AXI2:POS?")  # AXI1~2:POS?
            y = self.ser.read()
            y = int(y)
            print ('y is %d' % y)
            print (y)
            motorPosStr = "{} {}".format(x, y)#注意空格
            print(motorPosStr)  # 输出"100,200"  测试

            #motorPosStr = self.ser.read()  # type:object
            res = map(float, motorPosStr.strip().split())#motorPosStr.strip()是去除字符串前后的空格。并使用split()方法将其！！！按空格分割成一个字符串列表！！！
            res = list(map(float, motorPosStr.strip().split()))#使用map()函数将字符串列表中的元素转换为浮点型数据，并将转换后的数据存储到res列表中。
            print (res)
            # zuobiao = self.ser.read_raw().decode()  #最后返回res列表，该列表中存储了位移台的位置信息
            # print('zuobiao:%s' % (zuobiao.replace('\r', '')))#
        except Exception as e:
            print(e)
            print(motorPosStr)
            print('An Error has occured')
            self.showErr()
        return res


# 令motorPosStr=100,200
# res = map(float, motorPosStr.strip().split())
# print(res)        # <map object at 0x0000027A3A1C1E80>
# res_list = list(res)
# print(res_list)   # [100.0, 200.0]

# 或者
# res = list(map(float, motorPosStr.strip().split()))
# print(res)        # [100.0, 200.0]

    # 其中，{}
    # 是占位符，可以用变量的值来替换。format()
    # 方法可以将变量的值按照指定的格式填充到占位符中。在这个例子中，"{},{}"
    # 表示有两个占位符，分别对应两个变量的值。format(x, y)
    # 将变量x和y的值按照占位符的位置进行替换，从而得到最终的字符串
    # "100,200"。  解释：motorPosStr = "{},{}".format(x, y)
    #                  print(motorPosStr)  # 输出"100,200"


    def getPositionforRelativeMovement(self):
        return self.position



    def clear(self):
        try:
            self.ser.write('clear')
        except:
            self.showErr()


    def reset(self):  # Resets the whole device, equivalent of disconnecting the power according to the manual
        # a beep should be heard after the device is reset
        try:
            self.ser.write('*RST')
        except:
            self.showErr()



    def showErr(self):
        print('error')

rm = visa.ResourceManager()
print(rm.list_resources())
my_instrument = rm.open_resource('ASRL3::INSTR')#ASRL5::INSTR
a = CorvusEcoClass(my_instrument)
a.connect(my_instrument=my_instrument)

a.setVelocity(1)

a.setunit(1)#设置微米
a.getunit(1)
a.getunit(2)

#a.moveRelative(-1900,100)

a.moveX(500)
#a.moveY(5)

#a.moveAbsoluteXY(1000, 200)

time.sleep(4)
a.getPosition()



#a = CorvusEcolass
#a.connecct('ASRL5::INSTR', visa.ResourceManager, 1, 0, 2)
#init  --main--主函数