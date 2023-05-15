# -*- coding: utf-8 -*-
# The MIT License (MIT)

# Copyright (c) 2015 Michael Caverley

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

#MAIN ISSUES
#The Corvus does not return any errors for many things:
#e.g.: If an axis is not connected but is enabled through the code, everything will still proceed
#however, NONE of any of the axis will move when given the commmand (making it impossible to tell you which axis is not working)
#Corvus will tell you there is an internal error, but it does not give ANY details.

import time
import pyvisa as visa
import math

class CorvusEcoClass:
    NumberOfAxis = 2  # 定义轴数为2
    name = 'Corvus Eco'
    isSMU = False   #isSMU属性表示CorvusEcoClass类是否具有SMU（模拟输入输出）功能
    isMotor = True #是否具有电机功能
    isOpt = True  #是否具有光学功能
    isElec = False #电子
    isLaser = False #激光
    isDetect = False #检测


    def connect(self, visaName, rm, Velocity, Acceleration, NumberOfAxis):  # self,visaName,rm,速度,加速度,NumberOfAxis
         self.visaName = visaName
         self.ser = rm.open_resource('ASRL6::INSTR')#'ASRL3::INSTR'-->visaName
         self.ser.baud_rate = 9600
         self.ser.read_termination = '\r'
         self.ser.write_termination = '\r'
         self.ser.write('*IDN?')
         print(self.ser.read_raw().decode())
         print("Connected\n")
         
         # self.ser.write('AXIs 1~2')#选择坐标轴
         # self.ser.write(':UNIT 2') #p123页
         # print('Units are set to: Microns(um)\n')

    def disconnect(self):
        self.ser.close()
        print('Corvus Eco Disconnected')

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

    def setunit(self, unit):
        self.ser.write('AXI1:UNIT %d' % (unit))
        self.ser.write('AXI2:UNIT %d' % (unit))
        print('Units set successfully.')

    def getunit(self, AXI):  # 输入getunit（1）获取x轴单位
        self.ser.write('AXI%d:unit?' % AXI)
        get = self.ser.read()
        print ('AXI %d is setted to  ' % AXI + get)

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
    # def moveRelative(self, x, y=0, z=0):
    #     try:
    #         self.ser.write('AXI X:PULSe %.6f:GO 0' % x)   # %轴：参数：轴：参数
    #         self.ser.write('AXI Y:PULSe %.6f:GO 0' % y)
    #     except:
    #         print('An Error has occured')
    #         self.showErr()
    #     self.waitMoveComplete()
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

    def moveAbsoluteXYZ(self, x, y, z):#绝对位置移动
        self.ser.write('AXI1:GOABS %d' % x)
        self.ser.write('AXI2:GOABS %d' % y)

    def moveAbsoluteXY(self, x, y):#绝对位置移动
        self.ser.write('AXI1:GOABS %d' % x)
        self.ser.write('AXI2:GOABS %d' % y)

    def waitMoveComplete(self):
        while int(self.ser.query('MOTION?')) & 1:#读取步进电机的状态,1为正在移动，0为停止
            time.sleep(0.001)

    def getPosition(self):
        try:
            self.ser.write("AXI1:POS?")  # AXI1~2:POS?
            x = self.ser.read()
            #x = int(x)
            #print ('x is %d' % x)
            #print (x)

            self.ser.write("AXI2:POS?")  # AXI1~2:POS?
            y = self.ser.read()
            #y = int(y)
            #print ('y is %d' % y)
            #print (y)
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


















