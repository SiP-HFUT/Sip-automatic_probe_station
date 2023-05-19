# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 08:34:01 2023

@author: DELL_Zyf
"""

# import visa
import pyvisa as visa
import numpy as np
import time
import csv
from ctypes import *
from itertools import repeat
import hp816x_instr
import math;

# # 获取电压源和功率计的设备ID，可以通过NI MAX或者Visa Interactive Control来查看
# src_id = 'USB0::0x2A8D::0x1102::MY61004376::0::INSTR'
# pwr_id = 'USB0::0x0957::0x3718::MY48101370::0::INSTR'


class InstrumentConnection:
    def __init__(self, src_id, pwr_id, visa_interface='USB'):
        self.rm = visa.ResourceManager()
        self.src = self.rm.open_resource(src_id, timeout=10000)
        self.pwr = self.rm.open_resource(pwr_id, timeout=10000)
        print('连接成功：', self.src.query('*IDN?'), self.pwr.query('*IDN?'))

    def close(self):
        self.src.close()
        self.pwr.close()
        print('连接已关闭')
        
    def check_voltage_source_connection(self):
        """检查电压源连接状态"""
        try:
            idn = self.src.query("*IDN?")
            print("Connected to voltage source: {}".format(idn.strip()))
            return True
        except visa.VisaIOError:
            print("Failed to connect to voltage source!")
            return False

    def check_power_meter_connection(self):
        """检查功率计连接状态"""
        try:
            idn = self.pwr.query("*IDN?")
            print("Connected to power meter: {}".format(idn.strip()))
            return True
        except visa.VisaIOError:
            print("Failed to connect to power meter!")
            return False

class E36312AClass:
    def __init__(self):
        self.Aflag = False
        self.Bflag = False
        self.voltageresultA = []
        self.currentresultA = []
        self.voltageresultB = []
        self.currentresultB = []
        
        self.sweepcompletedflag = False  
        self.automeasureflag = True
        
    def connect(self, visaName, rm):
        rm = visa.ResourceManager()
        self.visaName = visaName
        
        self.inst = rm.open_resource(visaName)
        print(self.inst.query("*IDN?\n"))
        self.inst.write("SYST:BEEP:IMM 2400,0.1")#立即触发蜂鸣器响应；2400表示蜂鸣器的频率为2400Hz；0.1表示蜂鸣器响铃的时间为0.1秒
        
        time.sleep(0.25)
        self.inst.write("SYST:BEEP:IMM 2400,0.1")
        self.inst.write("*RST")                  #将设备的所有设置恢复为出厂默认值,确保在进行下一次测试前，设备处于初始状态。
        self.inst.write("*CLS")                  #清除设备内部的错误状态，清空输出缓存区的数据，以确保设备处于初始状态。
        print('Connected\n')

    def testconnection(self, rm):
        print(self.visaName)
        test = rm.open_resource(self.visaName)
        result = test.query("*IDN?\n")
        if result:
            print('Device is connected, no errors')
        else:
            print('Voltage source: E36312A cannot connect')

    def disconnect(self):
        self.inst.write("OUTPut OFF")
        #关闭E36312A电源的所有通道的输出
        print('E36312A Disconnected')
        
    def setVoltageandCurrent(self, voltage, current, channel):
        if channel == 'CH1':
            self.inst.write("APPLy CH1, {:f}, {:f}".format(voltage, current))
            print('Set channel 1 voltage to {:.2f}V and current to {:.2f}A'.format(voltage, current))
        if channel == 'CH2':
            self.inst.write("APPLy CH2, {:f}, {:f}".format(voltage, current))
            print('Set channel 2 voltage to {:.2f}V and current to {:.2f}A'.format(voltage, current))
        if channel == 'ALL':
            self.inst.write("APPLy ALL, {:f}, {:f}".format(voltage, current))
            print('Set both channels voltage to {:.2f}V and current to {:.2f}A'.format(voltage, current))
        
    def setcurrentlimit(self, currentlimit, channel):
        """
        Sets the current limit 
        """
        if channel == 'CH1':
            currentlimitstring = "SOURce:CURRent:PROTection:LEVel CH1, {:.3f}".format(currentlimit/1000)  # 设置CH1通道的电流限制
            self.inst.write(currentlimitstring)
            print("Set channel 1 current limit to " + str(currentlimit) + "mA")
        
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
        
    def getcurrentA(self):
        i = self.inst.query("print(MEASure:CURRent? CH1)")
        return i

    def getvoltageB(self):
        v = self.inst.query("print(MEASure:VOLTage? CH2)")
        return v

    def getcurrentB(self):
        i = self.inst.query("print(MEASure:CURRent? CH2)")
        return i
    def ivsweep(self, minVar, maxVar, resolution, independantvar):
        self.voltageresultA = []
        self.currentresultA = []
        self.voltageresultB = []
        self.currentresultB = []
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
                    self.inst.write("VOLTage v")
                    #VOLTage <v>，其中<v>为需要设置的电压值
                    i = self.inst.query("print(MEASure:CURRent:DC? CH1)")
                    i = float(i) * 1000
                    p = self.inst.query("print(MEASure:POWer:DC? CH1)")
                    p = float(p) * 1000
                    self.voltageresultA.append(v)
                    self.currentresultA.append(i)
                    self.powerresultA.append(p)
                    time.sleep(1)

            if self.Aflag == True:
                self.inst.write("INSTrument:NSELect 1")
                self.inst.write("FUNCtion:MODE VOLTage")
                self.inst.write("VOLTage 0")  
                
            if self.Bflag == True:
                self.inst.write("INSTrument:NSELect 2")
                self.inst.write("FUNCtion:MODE VOLTage")

                for v in sweeplist:
                    self.inst.write("VOLTage v")
                    i = self.inst.query("print(MEASure:CURRent:DC? CH2)")
                    i = float(i) * 1000
                    p = self.inst.query("print(MEASure:POWer:DC? CH2)")
                    p = float(p) * 1000
                    self.voltageresultB.append(v)
                    self.currentresultB.append(i)
                    self.powerresultB.append(p)
                    time.sleep(1)

            if self.Bflag == True:
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
                self.inst.write("INSTrument:NSELect 1")
                self.inst.write("FUNCtion:MODE CURRent")
                for i in sweeplist:
                    self.inst.write("CURRent i")
                    
                    v = self.inst.query("print(MEASure:VOLTage:DC? CH1)")
                    v = float(v)
                    p = self.inst.query("print(MEASure:POWer:DC? CH1)")
                    p = float(p) * 1000
                    self.voltageresultA.append(v)
                    self.currentresultA.append(i*1000)
                    self.powerresultA.append(p)
                    time.sleep(1)

            if self.Aflag == True:
                self.inst.write("INSTrument:NSELect 1")
                self.inst.write("FUNCtion:MODE CURRent")
                self.inst.write("CURRent 0")

            if self.Bflag == True:
                self.inst.write("INSTrument:NSELect 2")
                self.inst.write("FUNCtion:MODE CURRent")

                for i in sweeplist:
                    self.inst.write("CURRent i")
                    
                    v = self.inst.query("print(MEASure:VOLTage:DC? CH1)")
                    v = float(v)
                    p = self.inst.query("print(MEASure:POWer:DC? CH1)")
                    p = float(p) * 1000
                    self.voltageresultA.append(v)
                    self.currentresultA.append(i)
                    self.powerresultA.append(p)
                    time.sleep(1)

            if self.Bflag == True:
                self.inst.write("INSTrument:NSELect 2")
                self.inst.write("FUNCtion:MODE CURRent")
                self.inst.write("CURRent 0")

        print('Sweep Completed!')
    def turnchannelon(self, channel):
        if channel == 'CH1':
            # self.inst.write("smua.source.output = smua.OUTPUT_ON")
            self.inst.write("OUTPut CH1, ON")
            self.onflagA = 'ON'
            self.Aflag = True

        if channel == 'CH2':
            self.inst.write("OUTPut CH2, ON")
            self.onflagB = 'ON'
            self.Bflag = True

        if channel == 'ALL':
            self.inst.write("OUTPut ALL, ON")
            self.onflagA = 'ON'
            self.onflagB = 'ON'
            self.Aflag = True
            self.Bflag = True

    def turnchanneloff(self, channel):

        if channel == 'CH1':
            self.inst.write("OUTPut CH1, OFF")
            self.Aflag = False

        if channel == 'CH2':
            self.inst.write("OUTPut CH2, OFF")
            self.Bflag = False

        if channel == 'ALL':
            self.inst.write("OUTPut ALL, OFF")
            self.Aflag = False
            self.Bflag = False

    def setoutputflagon(self, channel):
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
    """Another"""
    def select_channel(self, channel_num):
        self.channel = channel_num
        self.src.write('INST:NSEL {}'.format(channel_num))
        print("Selected channel: {}".format(channel_num))

    def set_output(self, state):
        """将所选通道的输出设置为ON或OFF"""
        if state == 'ON':
            self.src.write('OUTP ON')
            print("Channel {} output set to ON".format(self.channel))
        elif state == 'OFF':
            self.src.write('OUTP OFF')
            print("Channel {} output set to OFF".format(self.channel))
        else:
            print("Invalid state input. Please enter either 'ON' or 'OFF'.")

    def set_channel_output(self, channel_num, output_status):
        """
        设置所选通道的输出状态。
        :param channel_num: 通道号。
        :param output_status: 输出状态，True表示ON，False表示OFF。
        """
        self.src.write('INST:NSEL {}'.format(channel_num))
        if output_status:
            self.src.write('OUTP ON')
        else:
            self.src.write('OUTP OFF')

    def set_voltage(self, voltage):
        self.src.write('VOLT {}'.format(voltage))

    def measure_voltage_current(self):
        self.src.write('MEAS:VOLT?')
        voltage = float(self.src.read())
        print("Current Voltage: {} V".format(voltage))
        self.src.write('MEAS:CURR?')
        current = float(self.src.read())
        print("Current Current: {} A".format(current))
        return voltage, current

    def measure_power(self):
        """测量电源和功率计的实时功率"""
        self.src.write('MEAS:POW?')
        time.sleep(1)
        voltage_power = float(self.src.read())
        print("Voltage Source Power: {} W".format(voltage_power))
        self.pwr.write('READ?')
        time.sleep(1)
        power = float(self.pwr.read())
        print("Power Meter Power: {} W".format(power))
        return voltage_power, power


class E_O_data:
    def measure_voltage_power(self, start_voltage, end_voltage, step_voltage, delay, file_name):
        # 创建一个CSV文件
        with open(file_name, 'wb') as f:
        # with open(file_name, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Voltage (V)', 'Source Power (W)', 'PowerMeter (W or dB?)'])
            voltage_array = np.arange(start_voltage, end_voltage + step_voltage, step_voltage)
            # 在给定的范围内循环调整电压，并记录相应的功率值
            for voltage in range(int(start_voltage * 10), int((end_voltage + step_voltage) * 10), int(step_voltage * 10)):
                voltage = voltage / 10.0

            # for voltage in range(start_voltage, end_voltage+step_voltage, step_voltage):
                self.set_voltage(voltage)
                time.sleep(delay)
                source_power = float(self.src.query('MEAS:POW?'))
                meter_power = self.measure_power()
                writer.writerow([voltage, source_power, meter_power])
                

src_id = 'USB0::0x2A8D::0x1102::MY61004376::0::INSTR'
pwr_id = 'USB0::0x0957::0x3718::MY48101370::0::INSTR'

# e36312a.setVoltageandCurrent(0.25, 0.2, 'CH1')

if __name__ == '__main__':
    conn = InstrumentConnection(src_id, pwr_id)

    # 检查电压源连接状态
    if not conn.check_voltage_source_connection():
        exit()
    # 检查功率计连接状态
    if not conn.check_power_meter_connection():
        exit()

    # rm = visa.ResourceManager()
    # visaName = src_id
    # e36312a = E36312AClass()
    # e36312a.connect(visaName, rm)
    # conn.select_channel(1)
    # conn.set_output('ON')
    # conn.set_channel_output(1, True)
    # conn.set_channel_output(2, False)
    # conn.set_voltage(0.025)
    # conn.measure_voltage_current()
    # conn.measure_source_power()
    # conn.measure_power()

    # conn.measure_voltage_power(0.0, 6.0, 0.1, 0.001, 'data.csv')
    # conn.close()
    
#     # conn.measure_voltage_power(0, 10, 1, 1, 'data.csv')
#     # Note-for example:在0到10伏特的范围内以1伏特的步长测量电压和功率值，延时1s,并将结果写入名为data.csv的CSV文件中
#     # conn.set_voltage(3.0)
#     # power = conn.measure_power()
#     # print('功率测量结果：{} W'.format(power))

