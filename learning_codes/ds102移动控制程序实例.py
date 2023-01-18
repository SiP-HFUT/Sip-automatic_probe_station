import pyvisa as visa


class Lk:
    unit = ["pulse", "um", "mm", "deg", "mrad"]
    units = unit[0]

    def __init__(self, ser):
        self.ser = ser

    def connect(self, my_instrument):  # self,visaName,rm,速度,加速度,NumberOfAxis
        self.ser = my_instrument
        self.ser.baud_rate = 9600
        self.ser.read_termination = '\r'
        self.ser.write_termination = '\r'
        self.ser.write('*IDN?')
        print(self.ser.read_raw().decode())
        print("Connected\n")

    def disconnect(self):
        self.ser.close()
        print('Disconnected')

    # SELSP:0~9
    def setSELectSPeed(self, AXI, SELectSPeed):
        self.ser.write("AXI%d:SELSP %d" % (AXI, SELectSPeed))
        self.ser.write("AXI%d:SELectSPeed?" % AXI)
        response = self.ser.read_raw().decode()
        print("SELectSPeed set to: table " + response)

    # Lspeed,Fspeed,Rate,Srate:0~9
    # unit pps,unit pps,unit msec,unit %
    def setLspeed(self, AXI, Lspeed, num):
        self.ser.write("AXI%d:L%d %d" % (AXI, Lspeed, num))
        self.ser.write("AXI%d:L%d?" % (AXI, Lspeed))
        response = self.ser.read_raw().decode()
        print('Lspeed set to: ' + response.replace('\r', '') + ' %s/s\n' % self.units)

    def setFspeed(self, AXI, Fspeed, num):
        # self.ser.write("AXI%d:SELectSPeed?" % AXI)
        # response = self.ser.read_raw().decode()
        # # print('Fspeed set to: ' + response.replace('\r', '') + ' %s/s\n' % self.units)
        # response=int(response.replace('\r', ''))
        # self.ser.write("AXI%d:SELSP %d:F%d %d" % (AXI, response,Fspeed, num))
        self.ser.write("AXI%d:F%d %d" % (AXI, Fspeed, num))
        self.ser.write("AXI%d:F%d?" % (AXI, Fspeed))
        response = self.ser.read_raw().decode()
        print('Fspeed set to: ' + response.replace('\r', '') + ' %s/s\n' % self.units)

    def setRate(self, AXI, Rate, num):
        self.ser.write("AXI%d:R%d %d" % (AXI, Rate, num))
        self.ser.write("AXI%d:R%d?" % (AXI, Rate))
        response = self.ser.read_raw().decode()
        print('Rate set to: ' + response.replace('\r', '') + ' %s/s\n' % self.units)

    def setSrate(self, AXI, Srate, num):
        self.ser.write("AXI%d:S%d %d" % (AXI, Srate, num))
        self.ser.write("AXI%d:S%d?" % (AXI, Srate))
        response = self.ser.read_raw().decode()
        print('Srate set to: ' + response.replace('\r', '') + ' %s/s\n' % self.units)

    # UNIT:
    # 0⇒pulse
    # 1⇒um
    # 2⇒mm
    # 3⇒deg
    # 4⇒mrad
    def setUNIT(self, AXI, UNIT):
        self.units = self.unit[UNIT]
        self.ser.write("AXI%d:UNIT %d" % (AXI, UNIT))
        self.ser.write("AXI%d:unit?" % AXI)
        response = int(self.ser.read_raw().decode().replace('\r', ''))
        self.units=self.unit[response]
        print('UNIT set to: %d %s/s\n' % (response,self.units))

    def getunit(self, AXI):
        self.ser.write('AXI%d:unit?' % AXI)
        response = int(self.ser.read_raw().decode().replace('\r', ''))
        self.units=self.unit[response]
        print('Axis %d is set to unitvalue: %s' % (AXI, self.units))

    def GO(self, AXI, GO):
        self.ser.write("AXI%d:GO %d:DW" % (AXI, GO))
        # print("AXI%d:GO %d:DW" % (AXI, GO))
        self.ser.write("AXI%d:POS?" % AXI)
        response = self.ser.read_raw().decode()
        while True:
            self.ser.write("AXI%d:POS?" % AXI)
            a = self.ser.read_raw().decode()
            if response == a:
                break
            else:
                response = a
        print('AXI%d go to: '%AXI + response.replace('\r', '') + ' %s\n' % self.units)

    def GOABSolute(self, AXI, GOABS):
        self.ser.write("AXI%d:GOABS %d" % (AXI, GOABS))
        self.ser.write("DWait")
        self.ser.write("AXI%d:POS?" % AXI)
        response = self.ser.read_raw().decode()
        while True:
            self.ser.write("AXI%d:POS?" % AXI)
            a = self.ser.read_raw().decode()
            if response == a:
                break
            else:
                response = a
        print('AXI%d go to: ' % AXI + response.replace('\r', '') + ' %s\n' % self.units)

    def getPosition(self):
        self.ser.write("AXI1:POS?")
        x = self.ser.read_raw().decode()
        self.ser.write("AXI2:POS?")
        y = self.ser.read_raw().decode()
        print('坐标:%s %s,单位:%s' % (x.replace('\r', ''),y.replace('\r', ''),self.units) )



rm = visa.ResourceManager()
print(rm.list_resources())
my_instrument = rm.open_resource('ASRL8::INSTR')
a = Lk(my_instrument)
a.connect(my_instrument=my_instrument)

a.setSELectSPeed(2, 2)
a.setFspeed(2, 1, 1000)
a.setUNIT(2,1)
a.setFspeed(2, 1, 1000)

# my_instrument.write("AXI2:SELectSPeed?")
# print(my_instrument.read_raw().decode())
# my_instrument.write("AXI2:Fspeed1?")
# print(my_instrument.read_raw().decode())
# my_instrument.write("AXI2:unit?")
# print(my_instrument.read_raw().decode())

# my_instrument.write("AXI2:SELSP 2:F1 10000")
# my_instrument.write("AXI2:GOABS 0:DW")
a.GOABSolute(2, 0)
# a.GO(2,4)
a.getPosition()
a.getunit(2)

