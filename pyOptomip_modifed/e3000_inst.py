# -*- coding: utf-8 -*-
"""
Created on April 2023

@author: Zhengyanfeng-DELL
"""
from __future__ import division
import time
import pyvisa as visa
import math
#from keysight.e36xx_series import E36xxSeries

# from keithley2600 import Keithley2600
# from keithley2600 import ResultTable


class e3000Class():
    
    name = 'e3000'    #SMU->e3000
    isSMU = True
    isMotor = False
    isLaser = False
    isDetect = False
    isElec = False

    def __init__(self):
        # self.visaName = None
        self.Aflag = False
        self.Bflag = False
        self.voltageresultA = []
        self.currentresultA = []
        self.voltageresultB = []
        self.currentresultB = []
        #self.voltageresultA、self.currentresultA、self.voltageresultB、self.currentresultB
        #分别是四个列表，用于存储电压和电流的测量结果
        self.sweepcompletedflag = False  #布尔值变量，表示扫描完成的标志位状态，初始化为False
        self.automeasureflag = True      #布尔值变量，表示自动测量的标志位状态，初始化为True

    def connect(self, visaName, rm):
        self.rm = visa.ResourceManager()
        self.visaName = visaName
        self.inst = rm.open_resource(visaName)
        print(self.inst.query("*IDN?"))
        self.inst.write("SYST:BEEP:IMM 2400,0.1")
        time.sleep(0.25)
        self.inst.write("SYST:BEEP:IMM 2400,0.1")
        self.inst.write("*RST")
        self.inst.write("*CLS")
        print('Connected\n')

    # def connect(self, visaName, rm):
    #     rm = visa.ResourceManager()
    #     self.visaName = visaName
    #     self.inst = rm.open_resource(visaName)
    #     print(self.inst.query("*IDN?\n"))
    #     self.inst.write("SYST:BEEP:IMM 2400,0.1")
    #     time.sleep(0.25)
    #     self.inst.write("SYST:BEEP:IMM 2400,0.1")
    #     self.inst.write("*RST")
    #     self.inst.write("*CLS")
    #     print('Connected\n')

    def testconnection(self, rm):
        print(self.visaName)
        test = rm.open_resource(self.visaName)
        result = test.query("*IDN?")
        if result:
            print('Device is connected, no errors')
        else:
            print('Voltage source: e3000 cannot connect')

    def disconnect(self):
        self.inst.write("OUTPut OFF")
        #关闭E36312A电源的所有通道的输出
        print('e3000 Disconnected')

    # def setVoltage(self, voltage, current, channel):
    #     if channel == 'CH1':
    #         self.inst.write("APPLy CH1, {:f}, {:f}".format(voltage, current))
    #         print('Set channel 1 voltage to {:.2f}V'.format(voltage))

    #     if channel == 'CH2':
    #         self.inst.write("APPLy CH2, {:f}, {:f}".format(voltage, current))
    #         print('Set channel 2 voltage to {:.2f}V'.format(voltage))

    #     if channel == 'All':
    #         self.inst.write("APPLy ALL, {:f}, {:f}".format(voltage, current))
    #         print('Set both channels voltage to {:.2f}V'.format(voltage))

    def setVoltageandCurrent(self, voltage, current, channel):
        if channel == 'CH1':
            self.inst.write("APPLy CH1, {:f}, {:f}".format(voltage, current))
            print('Set channel 1 voltage to {:.2f}V and current to {:.2f}A'.format(voltage, current))
        if channel == 'CH2':
            self.inst.write("APPLy CH2, {:f}, {:f}".format(voltage, current))
            print('Set channel 2 voltage to {:.2f}V and current to {:.2f}A'.format(voltage, current))
        if channel == 'ALL':
            # self.inst.write("APPLy ALL, {:f}, {:f}".format(voltage, current))
            self.inst.write("APPLy CH1, {:f}, {:f}".format(voltage, current))
            self.inst.write("APPLy CH2, {:f}, {:f}".format(voltage, current))
            print('Set both channels voltage to {:.2f}V and current to {:.2f}A'.format(voltage, current))
        
    def setcurrentlimit(self, currentlimit, channel):
        """
        Sets the current limit 
        """
        if channel == 'CH1':
            currentlimitstring = "SOURce:CURRent:PROTection:LEVel CH1, {:.3f}".format(currentlimit/1000)  # 设置CH1通道的电流限制
            self.inst.write(currentlimitstring)
            print("Set channel 1 current limit to " + str(currentlimit) + "mA")
        # if channel == 'CH1':
        #     currentlimitstring = "smua.source.limiti = " + str(float(currentlimit / 1000))
        #     self.inst.write(currentlimitstring)
        #     print("Set channel A current limit to " + str(currentlimit) + "mA")

        if channel == 'CH2':
            currentlimitstring = "SOURce:CURRent:PROTection:LEVel CH2, {:.3f}".format(currentlimit/1000)  # 设置CH2通道的电流限制
            self.inst.write(currentlimitstring)
            print("Set channel 2 current limit to " + str(currentlimit) + "mA")

        if channel == 'ALL':
            currentlimitstring = "SOURce:CURRent:PROTection:LEVel ALL, {:.3f}".format(currentlimit/1000)  # 设置all通道的电流限制
            self.inst.write(currentlimitstring)
            print("Set channel ALL current limit to " + str(currentlimit) + "mA")
           

    def setvoltagelimit(self, voltagelimit, channel):
        """
        Sets the voltage limit of the smu
        """
        if channel == 'CH1':
            voltagelimitstring = "SOURce:VOLTage:PROTection:LEVel CH1, {:.3f}".format(voltagelimit)  # 设置CH1通道的电压限制
            self.inst.write(voltagelimitstring)
            print("Set channel 1 voltage limit to " + str(voltagelimit) + " V")
        # if channel == 'A':
        #     voltagelimitstring = "smua.source.limitv = " + str(voltagelimit)
        #     self.inst.write(voltagelimitstring)
        #     print("Set channel A voltage limit to " + str(voltagelimit) + " V")

        if channel == 'CH2':
            voltagelimitstring = "SOURce:VOLTage:PROTection:LEVel CH2, {:.3f}".format(voltagelimit)  # 设置CH2通道的电压限制
            self.inst.write(voltagelimitstring)
            print("Set channel 2 voltage limit to " + str(voltagelimit) + " V")
        if channel == 'ALL':
            voltagelimitstring = "SOURce:VOLTage:PROTection:LEVel ALL, {:.3f}".format(voltagelimit)  # 设置all通道的电压限制
            self.inst.write(voltagelimitstring)
            print("Set channel ALL voltage limit to " + str(voltagelimit) + " V")
    def setpowerlimit(self, powerlimit, channel):
        """
        Sets the power limit 
        """
        if channel == 'CH1':
            powerlimitstring = "SOURce:POWer:PROTection:LEVel CH1, {:.6f}".format(powerlimit/1000)  # 设置CH1通道的功率限制
            self.inst.write(powerlimitstring)
            print("Set channel 1 power limit to " + str(powerlimit) + " mW")
        # if channel == 'A':
        #     powerlimitstring = "smua.source.limitp = " + str(float(powerlimit / 1000))
        #     self.inst.write(powerlimitstring)
        #     print("Set channel A power limit to " + str(powerlimit) + " mW")

        if channel == 'CH2':
            powerlimitstring = "SOURce:POWer:PROTection:LEVel CH2, {:.6f}".format(powerlimit/1000)  # 设置CH1通道的功率限制
            self.inst.write(powerlimitstring)
            print("Set channel 2 power limit to " + str(powerlimit) + " mW")
        if channel == 'ALL':
            powerlimitstring = "SOURce:POWer:PROTection:LEVel ALL, {:.6f}".format(powerlimit/1000)  # 设置CH1通道的功率限制
            self.inst.write(powerlimitstring)
            print("Set channel ALL power limit to " + str(powerlimit) + " mW")

    def getvoltageA(self):
        v = self.inst.query("print(MEASure:VOLTage? CH1)")  # 查询CH1通道的输出电压
        return v
        # v = self.inst.query("print(smua.measure.v())")
        # return v
        """
        Queries the e3000 and returns the voltage measured at channel A
        Returns
        -------
        the voltage seen at channel A in volts(in hfut, A/B is CH1/2)
        """
    def getcurrentA(self):
        i = self.inst.query("print(MEASure:CURRent? CH1)")
        # i = self.inst.query("print(smua.measure.i())")
        return i

    def getvoltageB(self):
        v = self.inst.query("print(MEASure:VOLTage? CH2)")
        return v

    def getcurrentB(self):
        i = self.inst.query("print(MEASure:CURRent? CH2)")
        return i
    
        """
        Note:in hfut, Keysight E36312A电源并不支持直接测量输出电阻的功能
        """

    #def ivsweep(self, minVar:float, maxVar:float, resolution:float, independantvar):
    def ivsweep(self, minVar, maxVar, resolution, independantvar):
        """
        Performs a current sweep or a voltage sweep depending on inputs
        Parameters
        ----------
        min : the minimum value for the independent variable
        max : the maximum value for the independent variable
        resolution : the resolution to sweep with
        independantvar : whether or not the independent variable is current or voltage, string
        Returns
        -------
        """

        self.voltageresultA = []
        self.currentresultA = []
        self.voltageresultB = []
        self.currentresultB = []
        # self.resistanceresultA = []
        # self.resistanceresultB = []
        self.powerresultA = []
        self.powerresultB = []
        #初始化一系列用于存储扫描结果的列表


        if independantvar == 'Voltage':
            # 设置电压扫描范围
            self.inst.write('VOLTage:STARt 0')  # 设置扫描起始电压
            self.inst.write('VOLTage:STOP 5')  # 设置扫描终止电压
            self.inst.write('VOLTage:STEP 0.1')  # 设置扫描步长
            # 设置等待时间
            self.inst.write('TRIGger:SOURce TIMer')  # 设置触发源为计时器
            self.inst.write('TRIGger:TIMer 0.1')  # 设置等待时间为0.1秒
            # 扫描完成后保持输出状态
            self.inst.write('OUTPut ON')  # 打开输出
            self.inst.write('OUTPut:STATe ON')  # 设置输出状态为ON
            #E36312A电源不支持脉冲扫描功能
            
            #self.k.voltage_sweep_single_smu(self.k.smua, range(0, 61), t_int=0.1, delay=-1, pulsed=False)
            #调用self.k.voltage_sweep_single_smu()方法对电压进行扫描测量.
            #其中range(0, 61)表示从0V到60V扫描，t_int表示等待时间，
            #delay表示扫描完成后是否保持扫描结束时的电压输出状态，pulsed表示是否为脉冲扫描。
            sweeplist = [minVar]   #设置数组用于存储电压扫描的具体数值
            x = minVar             
            """
            minVar表示最小电压值，maxVar表示最大电压值，resolution表示电压扫描的步进值;
            通过while循环，不断将电压步进resolution/1000，直到达到maxVar;
            根据Aflag和Bflag的值，判断是否需要对A通道或B通道进行电压扫描;
            
             如果Aflag为True，则对A通道进行电压扫描。
             先将电压源设置为直流电压输出模式，然后分别对sweeplist中的每个值进行扫描测量，得到电流i、电阻r、功率p等结果，
             并将结果存储在voltageresultA、currentresultA、resistanceresultA、powerresultA四个列表中。
             如果Aflag为True，则将A通道电压源设置为0V.
            """
            while x < maxVar:
                sweeplist.append(x + resolution / 1000)
                x = x + resolution / 1000


            if self.Aflag == True:
                # self.inst.write("smua.source.func = smua.OUTPUT_DCVOLTS")
                self.inst.write("INSTrument:NSELect 1")#or following
                self.inst.write("FUNCtion:MODE VOLTage")
                #通道1设置为直流电压输出模式******
                for v in sweeplist:
                    # setvoltstring = "smua.source.levelv = " + str(v)
                    #setvoltstring = " f"VOLTage {v}" = " + str(v)  #是否可行？
                    # self.inst.write(setvoltstring)
                    
                    self.inst.write("VOLTage v")
                    #VOLTage <v>，其中<v>为需要设置的电压值
                    i = self.inst.query("print(MEASure:CURRent:DC? CH1)")
                    i = float(i) * 1000
                    # r = self.inst.query("print(smua.measure.r())")
                    # r = float(r)
                    p = self.inst.query("print(MEASure:POWer:DC? CH1)")
                    p = float(p) * 1000
                    self.voltageresultA.append(v)
                    self.currentresultA.append(i)
                    # self.resistanceresultA.append(r)
                    self.powerresultA.append(p)
                    # rt.append_row([v, i])
                    time.sleep(1)

            if self.Aflag == True:
                # setvoltstring = "smua.source.levelv = " + str(0)
                # self.inst.write(setvoltstring)
                
                self.inst.write("INSTrument:NSELect 1")
                self.inst.write("FUNCtion:MODE VOLTage")
                self.inst.write("VOLTage 0")  
                
            if self.Bflag == True:
                # self.inst.write("smub.source.func = smub.OUTPUT_DCVOLTS")
                self.inst.write("INSTrument:NSELect 2")
                self.inst.write("FUNCtion:MODE VOLTage")

                for v in sweeplist:
                    # setvoltstring = "smub.source.levelv = " + str(v)
                    # self.inst.write(setvoltstring)
                    self.inst.write("VOLTage v")
                    i = self.inst.query("print(MEASure:CURRent:DC? CH2)")
                    i = float(i) * 1000
                    # r = self.inst.query("print(smub.measure.r())")
                    # r = float(r)
                    p = self.inst.query("print(MEASure:POWer:DC? CH2)")
                    p = float(p) * 1000
                    self.voltageresultB.append(v)
                    self.currentresultB.append(i)
                    # self.resistanceresultB.append(r)
                    self.powerresultB.append(p)
                    time.sleep(1)

            if self.Bflag == True:
                # setvoltstring = "smub.source.levelv = " + str(0)
                # self.inst.write(setvoltstring)
                self.inst.write("INSTrument:NSELect 2")
                self.inst.write("FUNCtion:MODE VOLTage")
                self.inst.write("VOLTage 0")
                
                
        if independantvar == 'Current':

            sweeplist = [minVar / 1000]
            x = minVar / 1000

            while x < maxVar / 1000:
                sweeplist.append(x + resolution / 1000)
                x = x + resolution / 1000


            if self.Aflag == True:
                # self.inst.write("smua.source.func = smua.OUTPUT_DCAMPS")
                self.inst.write("INSTrument:NSELect 1")
                self.inst.write("FUNCtion:MODE CURRent")
                for i in sweeplist:
                    # setcurrentstring = "smua.source.leveli = " + str(i)
                    # self.inst.write(setcurrentstring)
                    self.inst.write("CURRent i")
                    
                    v = self.inst.query("print(MEASure:VOLTage:DC? CH1)")
                    v = float(v)
                    # r = self.inst.query("print(smua.measure.r())")
                    # r = float(r)
                    p = self.inst.query("print(MEASure:POWer:DC? CH1)")
                    p = float(p) * 1000
                    self.voltageresultA.append(v)
                    self.currentresultA.append(i*1000)
                    # self.resistanceresultA.append(r)
                    self.powerresultA.append(p)
                    # rt.append_row([v, i])
                    time.sleep(1)

            if self.Aflag == True:
                # setcurrentstring = "smua.source.leveli = " + str(0)
                # self.inst.write(setcurrentstring)
                self.inst.write("INSTrument:NSELect 1")
                self.inst.write("FUNCtion:MODE CURRent")
                self.inst.write("CURRent 0")

            if self.Bflag == True:
                # self.inst.write("smub.source.func = smub.OUTPUT_DCAMPS")
                self.inst.write("INSTrument:NSELect 2")
                self.inst.write("FUNCtion:MODE CURRent")

                for i in sweeplist:
                    # setcurrentstring = "smub.source.leveli = " + str(i)
                    # self.inst.write(setcurrentstring)
                    self.inst.write("CURRent i")
                    
                    v = self.inst.query("print(MEASure:VOLTage:DC? CH1)")
                    v = float(v)
                    # r = self.inst.query("print(smub.measure.r())")
                    # r = float(r)
                    p = self.inst.query("print(MEASure:POWer:DC? CH1)")
                    p = float(p) * 1000
                    self.voltageresultA.append(v)
                    self.currentresultA.append(i)
                    # self.resistanceresultA.append(r)
                    self.powerresultA.append(p)
                    # rt.append_row([v, i])
                    time.sleep(1)

            if self.Bflag == True:
                # setcurrentstring = "smub.source.leveli = " + str(0)
                # self.inst.write(setcurrentstring)
                self.inst.write("INSTrument:NSELect 2")
                self.inst.write("FUNCtion:MODE CURRent")
                self.inst.write("CURRent 0")

        print('Sweep Completed!')

    #def ivsweep2(self, minVar:float, maxVar:float, resolution:float, independantvar):
    def ivsweep2(self, minVar, maxVar, resolution, independantvar):
        """
                ivsweep2意欲何为？
                Performs a current sweep or a voltage sweep depending on inputs
                Parameters
                ----------
                min : the minimum value for the independent variable
                max : the maximum value for the independent variable
                resolution : the resolution to sweep with
                independantvar : whether or not the independent variable is current or voltage, string
                Returns
                -------
                """

        self.voltageresultA = []
        self.currentresultA = []
        self.voltageresultB = []
        self.currentresultB = []
        # self.resistanceresultA = []
        # self.resistanceresultB = []
        self.powerresultA = []
        self.powerresultB = []

        sweeplist = [minVar]
        x = minVar

        while x < maxVar:
            sweeplist.append(x + resolution / 1000)
            x = x + resolution / 1000

        if independantvar == 'Voltage':
            if self.Aflag == True:
                # self.voltageresultA, self.currentresultA = self.k.voltage_sweep_single_smu(self.k.smua, sweeplist, t_int=0.1, delay=-1, pulsed=False)
                # 该函数的作用是对SMU单通道进行电压扫描，并返回扫描的电压和电流数据。
                # self.k.smua：表示选择SMUA通道进行电压扫描。
                # sweeplist：表示需要扫描的电压列表，即SMU通道需要扫描的电压值序列。               
                # t_int=0.1：表示每次测量的积分时间，单位为秒，默认为0.1秒。                
                # delay=-1：表示扫描结束后的等待时间，单位为秒。当delay=-1时，表示等待时间为自动计算，即等待时间为扫描时间的两倍。               
                # pulsed=False：表示是否使用脉冲模式进行扫描。当pulsed=False时，表示使用DC模式进行扫描。
                voltage_list = [0.0] * len(sweeplist)
                current_list = [0.0] * len(sweeplist)
                for idx, voltage in enumerate(sweeplist):
                    
                    self.inst.write('SOURce CH1')
                    self.inst.write('SOURce:VOLTage:MODE FIXed')
                    self.inst.write('SOURce:VOLTage:LEVel:IMMediate:AMPLitude {voltage}'.format(voltage))
                    self.inst.write('OUTPut ON')
                    time.sleep(0.1)
                    voltage_list[idx] = float(self.inst.query('MEASure:VOLTage?'))
                    current_list[idx] = float(self.inst.query('MEASure:CURRent?'))
                    
                self.voltageresultA = voltage_list
                self.currentresultA = current_list
                
                # self.resistanceresultA = [i / j for i, j in zip(self.voltageresultA, self.currentresultA)]
                
                self.powerresultA = [i * j for i, j in zip(self.voltageresultA, self.currentresultA)]
                
                # setvoltstring = "smua.source.levelv = " + str(0)
                # self.inst.write(setvoltstring)
                self.inst.write("INSTrument:NSELect 1")
                self.inst.write("FUNCtion:MODE VOLTage")#这一句需要否
                self.inst.write("VOLTage 0")
            if self.Bflag == True:
                # self.voltageresultB, self.currentresultB = self.k.voltage_sweep_single_smu(self.k.smub, range(minVar, maxVar), t_int=0.1, delay=-1, pulsed=False)
                # self.resistanceresultA = self.voltageresultB / self.currentresultB
                voltage_list = [0.0] * len(sweeplist)
                current_list = [0.0] * len(sweeplist)
                for idx, voltage in enumerate(sweeplist):
                    
                    self.inst.write('SOURce CH2')
                    self.inst.write('SOURce:VOLTage:MODE FIXed')
                    self.inst.write('SOURce:VOLTage:LEVel:IMMediate:AMPLitude {voltage}'.format(voltage))
                    self.inst.write('OUTPut ON')
                    time.sleep(0.1)
                    voltage_list[idx] = float(self.inst.query('MEASure:VOLTage?'))
                    current_list[idx] = float(self.inst.query('MEASure:CURRent?'))
                    
                self.voltageresultB = voltage_list
                self.currentresultB = current_list
                self.powerresultB = self.voltageresultB * self.currentresultB
                # setvoltstring = "smub.source.levelv = " + str(0)
                # self.inst.write(setvoltstring)
                self.inst.write("INSTrument:NSELect 2")
                self.inst.write("FUNCtion:MODE VOLTage")#这一句需要否
                self.inst.write("VOLTage 0")

        
        if independantvar == 'Current':

            sweeplist = [minVar / 1000]
            x = minVar / 1000

            while x < maxVar / 1000:
                sweeplist.append(x + resolution / 1000)
                x = x + resolution / 1000


            if self.Aflag == True:
                # self.inst.write("smua.source.func = smua.OUTPUT_DCAMPS")
                self.inst.write("INSTrument:NSELect 1")
                self.inst.write("FUNCtion:MODE CURRent")
                for i in sweeplist:
                    # setcurrentstring = "smua.source.leveli = " + str(i)
                    # self.inst.write(setcurrentstring)
                    self.inst.write("CURRent i")

                    v = self.inst.query("print(MEASure:VOLTage:DC? CH1)")
                    v = float(v)
                    # r = self.inst.query("print(smua.measure.r())")
                    # r = float(r)
                    p = self.inst.query("print(MEASure:POWer:DC? CH1)")
                    p = float(p) * 1000
                    self.voltageresultA.append(v)
                    self.currentresultA.append(i*1000)
                    # self.resistanceresultA.append(r)
                    self.powerresultA.append(p)
                    # rt.append_row([v, i])
                    time.sleep(1)

            if self.Aflag == True:
                # setcurrentstring = "smua.source.leveli = " + str(0)
                # self.inst.write(setcurrentstring)
                self.inst.write("INSTrument:NSELect 1")
                self.inst.write("FUNCtion:MODE CURRent")
                self.inst.write("CURRent 0")


            if self.Bflag == True:
                # self.inst.write("smub.source.func = smub.OUTPUT_DCAMPS")
                self.inst.write("INSTrument:NSELect 2")
                self.inst.write("FUNCtion:MODE CURRent")

                for i in sweeplist:
                    # setcurrentstring = "smub.source.leveli = " + str(i)
                    # self.inst.write(setcurrentstring)
                    self.inst.write("CURRent i")

                    v = self.inst.query("print(MEASure:VOLTage:DC? CH2)")
                    v = float(v)
                    # r = self.inst.query("print(smub.measure.r())")
                    # r = float(r)
                    p = self.inst.query("print(MEASure:POWer:DC? CH2)")
                    p = float(p) * 1000
                    self.voltageresultA.append(v)
                    self.currentresultA.append(i)
                    # self.resistanceresultA.append(r)
                    self.powerresultA.append(p)
                    # rt.append_row([v, i])
                    time.sleep(1)

            if self.Bflag == True:
                # setcurrentstring = "smub.source.leveli = " + str(0)
                # self.inst.write(setcurrentstring)
                self.inst.write("INSTrument:NSELect 2")
                self.inst.write("FUNCtion:MODE CURRent")
                self.inst.write("CURRent 0")

        self.sweepcompletedflag = True

    def turnchannelon(self, channel):
        """
        Configures the specified channel to be on
        Parameters
        ----------
        channel : the channel that wants to be turned on
        Returns
        -------
        A print statement indicating that the channel specified has been turned on
        """

        if channel == 'CH1':
            # self.inst.write("smua.source.output = smua.OUTPUT_ON")
            self.inst.write("OUTP 1, (@1)")
            self.onflagA = 'ON'
            self.Aflag = True

        if channel == 'CH2':
            self.inst.write("OUTP 1, (@2)")
            self.onflagB = 'ON'
            self.Bflag = True

        if channel == 'ALL':
            # self.inst.write("smua.source.output = smua.OUTPUT_ON")
            # self.onflagA = 'ON'
            # self.Aflag = True
            # self.inst.write("smub.source.output = smub.OUTPUT_ON")
            # self.onflagB = 'ON'
            # self.Bflag = True
            self.inst.write("OUTP ON, (@1,2)")##OUTP ON, (@1,2,3) is also OK
            self.onflagA = 'ON'
            self.onflagB = 'ON'
            self.Aflag = True
            self.Bflag = True

    def turnchanneloff(self, channel):
        """
        Configures the specified channel to be off
        Parameters
        ----------
        channel : the channel that wants to be turned off
        Returns
        -------
        A print statement indicating that the channel specified has been turned off
        """

        if channel == 'CH1':
            # self.inst.write("smua.source.output = smua.OUTPUT_OFF")
            self.inst.write("OUTP 0, (@1)")
            self.Aflag = False

        if channel == 'CH2':
            self.inst.write("OUTP 0, (@2)")
            self.Bflag = False

        if channel == 'ALL':
            # self.inst.write("smua.source.output = smua.OUTPUT_OFF")
            # self.Aflag = False
            # self.inst.write("smub.source.output = smub.OUTPUT_OFF")
            # self.Bflag = False
            self.inst.write("OUTP OFF, (@1,2)")
            # self.onflagA = 'OFF'
            # self.onflagB = 'OFF'
            self.Aflag = False
            self.Bflag = False

    def setoutputflagon(self, channel):
        """
        Sets the channel for use in sweep
        Parameters
        ----------
        channel : the channel to be used in the sweep
        Returns
        -------
        A print statement letting the user know the channel has been set for use with sweep
        """

        if channel == 'CH1':
            self.Aflag = True
            print("Channel 1 set for use with sweep")
        if channel == 'CH2':
            self.Bflag = True
            print("Channel 2 set for use with sweep")
        if channel == 'ALL':
            self.Aflag =True
            self.Bflag = True
            print("Channel 1 set for use with sweep")
            print("Channel 2 set for use with sweep")

    def setoutputflagoff(self, channel):
        """
        Unsets a channel for use in sweep
        Parameters
        ----------
        channel : the channel to be unset for use in the sweep
        Returns
        -------
        A print statement letting the user know the channel has been unset for use with sweep
        """

        if channel == 'CH1':
            self.Aflag = False
            print("Channel 1 disabled for use with sweep")
        if channel == 'CH2':
            self.Bflag = False
            print("Channel 2 disabled for use with sweep")
        if channel == 'ALL':
            self.Aflag = False
            self.Bflag = False
            print("Channel 1 disabled for use with sweep")
            print("Channel 2 disabled for use with sweep")

######TEST FUNCTION and SCPI Commands#####
# rm = visa.ResourceManager()
# visaName = 'USB0::0x2A8D::0x1102::MY61004376::0::INSTR'#USB0::0x2A8D::0x1102::MY61004376::0::INSTR
# my_test = e3000Class()
# my_test.connect(visaName, rm)
# my_test.setVoltageandCurrent(0.5, 0.5, 'ALL')
# my_test.testconnection(rm)
# my_test.disconnect()
# my_test.turnchannelon('CH2')
# my_test.turnchanneloff('ALL')
# my_test.setoutputflagon('ALL')
# my_test.setoutputflagoff('ALL')
# if __name__ == '__main__':
#     rm = visa.ResourceManager()
#     visaName = 'USB0::0x2A8D::0x1102::MY61004376::0::INSTR'
#     my_test = e3000Class()
#     if my_test.connect(visaName, rm):
#         print("Connection successful")
#     else:
#         print("Connection failed")
        
#     # channel = 'CH1'   
#     # mytest.turnchannelon()
#     # mytest.turnchanneloff()
#     # mytest.setVoltageandCurrent(0.5, 0.5, channel)