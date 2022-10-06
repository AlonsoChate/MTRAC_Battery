from serialUtility import serUtil
from config import inst

class batteryModule:
    def __init__(self):
        # configure serial here
        self.serial = serUtil('/dev/ttyUSB0', 612500, 5, 5)
        # volt & temp
        self.cellVolt = [0] * 6
        self.moduleVolt = 0
        self.temperature = [0] * 2
        self.moduleAddr = 0
        # status
        self.alerts = 0
        self.faults = 0
        self.COVFaults = 0
        self.CUVFaults = 0

    def reset(self):
        command = bytes([0x3F << 1]) + bytes([0x3C]) + bytes([0xA5])

        response = self.serial.query(command, 4, True)
        pass

    def readStatus(self):
        # read any alerts or faults
        addr = bytes([self.moduleAddr << 1])
        command = addr + bytes([inst['REG_ALERT_STATUS']]) + bytes([0x04])
        response = self.serial.query(command, 7, False)
        self.alerts = response[3]
        self.faults = response[4]
        self.COVFaults = response[5]
        self.CUVFaults = response[6]
        pass

    def readValues(self):
        # read temperature and voltage
        addr = bytes([self.moduleAddr << 1])
        self.readStatus()

        # ADC Auto mode, read every ADC input we can (Both Temps, Pack, 6 cells)
        command = addr + bytes([inst['REG_ADC_CTRL']]) + bytes([0b00111101])
        self.serial.query(command, 3, True)

        # enable temperature measurement VSS pins
        command = addr + bytes([inst['REG_IO_CTRL']]) + bytes([0b00000011])
        self.serial.query(command, 3, True)

        # start all ADC conversions
        command = addr + bytes([inst['REG_ADC_CONV']]) + bytes([0b1])
        self.serial.query(command, 3, True)

        # start reading registers at the module voltage registers
        # read 18 bytes
        # 2 bytes each for ModuleV, CellV 1-6, Temp1, Temp2
        command = addr + bytes([inst['REG_GPAI']]) + bytes([0x12]) 
        response = self.serial.query(command, 22, False)

        # response bytes composed of:
        # 0: address
        # 1: command
        # 2: requested number of values
        # 3-20: value
        # 21: CRC check
        CRC = self.serial.genCRC(response[:-1])
        if response[0] == addr and response[1] == inst['REG_GPAI'] \
        and response[3] == 0x12 and response[4] == CRC:
            # TODO:
            pass
    
    def balance(self):
        # TODO:
        pass