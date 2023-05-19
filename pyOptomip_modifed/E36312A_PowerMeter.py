# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 08:34:01 2023

@author: DELL_Zyf
"""

# import visa
import pyvisa as visa
import numpy as np
import scipy.io as sio
import time
import matplotlib.pyplot as plt


class InstrumentConnection:
    def __init__(self, src_id, pwr_id, visa_interface='USB'):
        self.rm = visa.ResourceManager()
        self.src = self.rm.open_resource(src_id)
        self.pwr = self.rm.open_resource(pwr_id)
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
        # print("Current Voltage: {} V".format(voltage))
        self.src.write('MEAS:CURR?')
        current = float(self.src.read())
        # print("Current Current: {} A".format(current))
        return voltage, current

    def measure_power(self, slot_no):
        """测量电源和功率计的实时功率"""
        # self.src.write('MEAS:POW?')
        v, i = self.measure_voltage_current()
        time.sleep(1)
        voltage_power = v * i
        # voltage_power = float(self.src.read())
        # print("Voltage Source Power: {} W".format(voltage_power))

        self.pwr.write('sens1:pow:unit 0')
        time.sleep(1)
        self.pwr.write('sens1:pow:rang:auto 0')

        # self.pwr.write('sens1:pow:rang:auto?')
        # auto_range_mode = self.pwr.read()
        # print("Auto range mode opend? (1/0): {} ".format(auto_range_mode))
        command_str = 'sens' + str(slot_no) + ':pow:atim 0.1s'
        self.pwr.write(command_str)
        # self.pwr.write('sens1:pow:atim 0.1s')

        # self.pwr.write('sens1:pow:atim?')
        # ave_t = self.pwr.read()
        # print("CUrrent average time: {} s".format(ave_t))

        self.pwr.write(':READ1:POWer?')
        # time.sleep(1)  ':READ1:POWer?'
        power = float(self.pwr.read())
        # print("Power Meter Power: {} dBm".format(power))
        return voltage_power, power
    def connect(self, visaName, rm):
        # rm = visa.ResourceManager()#zyf:Yes or no is this statement required here?
        self.visaName = visaName

        self.inst = rm.open_resource(visaName)
        print(self.inst.query("*IDN?\n"))
        self.inst.write("SYST:BEEP:IMM 2400,0.1")  # 立即触发蜂鸣器响应；2400表示蜂鸣器的频率为2400Hz；0.1表示蜂鸣器响铃的时间为0.1秒
        # self.inst.write("delay(0.250)")         #Wait 250 milliseconds
        time.sleep(0.25)
        self.inst.write("SYST:BEEP:IMM 2400,0.1")
        self.inst.write("*RST")  # 将设备的所有设置恢复为出厂默认值,确保在进行下一次测试前，设备处于初始状态。
        self.inst.write("*CLS")  # 清除设备内部的错误状态，清空输出缓存区的数据，以确保设备处于初始状态。
        # self.inst.write("dataqueue.clear()")
        # self.inst.write("errorqueue.clear()")

        print('Connected\n')
    def measure_voltage_power(self, start_voltage, end_voltage, step_voltage, delay, file_name):

        voltages = []
        currents = []
        powerE = []
        powers = []

        # 计算设置电压的步数
        num_steps = int((end_voltage - start_voltage) / step_voltage) + 1

        # 在电压范围内循环设置电压
        for i in range(num_steps):
            # 计算当前电压值
            voltage = start_voltage + i * step_voltage
            # 设置电压
            self.set_voltage(voltage)
            # 延时
            time.sleep(delay)
            # 测量电压和电流
            v, i = self.measure_voltage_current()
            # 计算功率
            p = v * i
            _, power = self.measure_power()
            # 将电压、电流、功率添加到列表中
            voltages.append(voltage)
            currents.append(i)
            powerE.append(p)
            powers.append(power)

        # 将数据保存到.mat文件中
        data = {'voltage': np.array(voltages), 'current': np.array(currents), 'powerE': np.array(powerE), 'power': np.array(powers)}
        sio.savemat(file_name, data)
        return voltages, currents, powerE, powers

    # def measure_voltage_power(self, start_voltage, end_voltage, step_voltage, delay, file_name):
    #     # 创建一个CSV文件
    #     with open(file_name, 'wb') as f:
    #     # with open(file_name, 'w', newline='') as f:
    #         writer = csv.writer(f)
    #         writer.writerow(['Voltage (V)', 'Source Power (W)', 'PowerMeter (dBm)'])
    #         voltage_array = np.arange(start_voltage, end_voltage + step_voltage, step_voltage)
    #         # 在给定的范围内循环调整电压，并记录相应的功率值
    #         for voltage in range(int(start_voltage * 10), int((end_voltage + step_voltage) * 10), int(step_voltage * 10)):
    #             voltage = voltage / 10.0
    #
    #         # for voltage in range(start_voltage, end_voltage+step_voltage, step_voltage):
    #             self.set_voltage(voltage)
    #             time.sleep(delay)
    #             source_power = float(self.src.query('MEAS:POW?'))
    #             meter_power = self.measure_power()
    #             writer.writerow([voltage, source_power, meter_power])
src_id = 'USB0::0x2A8D::0x1102::MY61004376::0::INSTR'
pwr_id = 'USB0::0x0957::0x3718::MY48101370::0::INSTR'

if __name__ == '__main__':
    conn = InstrumentConnection(src_id, pwr_id)
    voltages = []
    powers = []

    # rm = visa.ResourceManager()
    # visaName = 'USB0::0x2A8D::0x1102::MY61004376::0::INSTR'
    # conn.connect(visaName, rm)
    # 检查电压源连接状态
    if not conn.check_voltage_source_connection():
        exit()
    # 检查功率计连接状态
    if not conn.check_power_meter_connection():
        exit()
    # conn.select_channel(1)
    # conn.set_output('ON')
    # conn.set_channel_output(1, True)
    # conn.set_channel_output(2, False)
    # conn.set_voltage(0.025)
    # conn.measure_voltage_current()
    # conn.measure_power()
    # voltages, currents, powerE, powers = conn.measure_voltage_power(0.0, 1.0, 0.5, 0.001, 'data1')
    # # conn.measure_voltage_power(0.0, 1.0, 0.1, 0.001, 'data1')
    # # print(voltages)
    # # print(powers)
    # # 绘制电压-功率图
    # plt.plot(voltages, powers)
    # # 添加标签
    # plt.xlabel('Voltage (V)')
    # plt.ylabel('Power (dBm)')
    # plt.title('Voltage-Power  Plot')
    # # 显示图形
    # plt.show()
    # # conn.close()

#     # conn.measure_voltage_power(0, 10, 1, 1, 'data.csv')
#     # Note-for example:在0到10伏特的范围内以1伏特的步长测量电压和功率值，延时1s,并将结果写入名为data.csv的CSV文件中
#     # conn.set_voltage(3.0)
#     # power = conn.measure_power()
#     # print('功率测量结果：{} W'.format(power))

