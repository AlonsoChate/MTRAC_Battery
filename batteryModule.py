from serialUtility import Ser, inst
from math import log

class batteryModule:
    def __init__(self):
        # volt & temp
        self.cellVolt = [0] * 6
        self.cellBalance = [False] * 6
        self.moduleVolt = 0
        self.temperature = [0] * 2
        self.moduleAddr = 0
        # status
        self.alerts = 0
        self.faults = 0
        self.COVFaults = 0
        self.CUVFaults = 0
        self.isBalanced = False

    def readStatus(self):
        # read any alerts or faults
        addr = bytes([self.moduleAddr << 1])
        command = addr + bytes([inst['REG_ALERT_STATUS']]) + bytes([0x04])
        response = Ser.query(command, 7, False)
        self.alerts = response[3]
        self.faults = response[4]
        self.COVFaults = response[5]
        self.CUVFaults = response[6]

    def readValues(self):
        # read temperature and voltage
        addr = bytes([self.moduleAddr << 1])
        self.readStatus()

        # ADC Auto mode, read every ADC input we can (Both Temps, Pack, 6 cells)
        command = addr + bytes([inst['REG_ADC_CTRL']]) + bytes([0b00111101])
        Ser.query(command, 3, True)

        # enable temperature measurement VSS pins
        command = addr + bytes([inst['REG_IO_CTRL']]) + bytes([0b00000011])
        Ser.query(command, 3, True)

        # start all ADC conversions
        command = addr + bytes([inst['REG_ADC_CONV']]) + bytes([0b1])
        Ser.query(command, 3, True)

        # start reading registers at the module voltage registers
        # read 18 bytes
        # 2 bytes each for ModuleV, CellV 1-6, Temp1, Temp2
        command = addr + bytes([inst['REG_GPAI']]) + bytes([0x12]) 
        response = Ser.query(command, 22, False)

        # response bytes composed of:
        # 0: address
        # 1: command
        # 2: requested number of values
        # 3-20: value
        # 21: CRC check
        CRC = Ser.genCRC(response[:-1])
        if response[0] == addr and response[1] == inst['REG_GPAI'] \
        and response[3] == 0x12 and response[4] == CRC:
            self.moduleVolt = (response[3]*256+response[4])*0.002034609
            for i in range(6):
                self.cellVolt[i] = (response[5+i*2]*256 + response[6+i*2])*0.000381493
            self.temperature[0] = self.calTemp(response[17], response[18])
            self.temperature[1] = self.calTemp(response[19], response[20])
            print("Successfully read temp and voltages")
            return True
        print("Invalid response for readValue()")
        return False
        
    def calTemp(self, left:int, right:int):
        # calculate the temperature given reading from readValues()
        # use steinhart/hart equation
        temp = (1.78/((left*256+right+2)/33046)-3.57)*1000
        result = 1/(0.0007610373573+(0.0002729524832*log(temp))+log(temp)**3*0.0000001022822735)
        return result - 273.15

    def balance(self):
        # balance point
        balanceVolt = 3.9

        addr = bytes([self.moduleAddr << 1])
        # resets balance time and should be done before setting balance resistors again
        command = addr + bytes([inst['REG_BAL_CTRL']]) + bytes([0])
        Ser.query(command, 30, True)
        
        