from time import sleep
from serial import Serial

# the serial is assigned at the end of the file

# to make pyserial work, either give read and write permission to the virtual driver
# or add current user to group dialout
# $sudo usermod -a -G dialout <username>

# all address of registers
inst = {
    'REG_DEV_STATUS'    :   0,
    'REG_GPAI'          :   1,
    'REG_VCELL1'        :   3,
    'REG_VCELL2'        :   5,
    'REG_VCELL3'        :   7,
    'REG_VCELL4'        :   9,
    'REG_VCELL5'        :   0xB,
    'REG_VCELL6'        :   0xD,
    'REG_TEMPERATURE1'  :   0xF,
    'REG_TEMPERATURE2'  :   0x11,
    'REG_ALERT_STATUS'  :   0x20,
    'REG_FAULT_STATUS'  :   0x21,
    'REG_COV_FAULT'     :   0x22,
    'REG_CUV_FAULT'     :   0x23,
    'REG_ADC_CTRL'      :   0x30,
    'REG_IO_CTRL'       :   0x31,
    'REG_BAL_CTRL'      :   0x32,
    'REG_BAL_TIME'      :   0x33,
    'REG_ADC_CONV'      :   0x34,
    'REG_ADDR_CTRL'     :   0x3B,
    'MAX_MODULE_ADDR'   :   0x3E
}

class serUtil:
    def __init__(self, portname, baudrate=9600, readTimeOut=None, writeTimeOut=None):
        self.portname = portname
        self.baudrate = baudrate
        self.readTimeOut = readTimeOut
        self.writeTimeOut = writeTimeOut
        # without timeout read or write will block
        self.ser = Serial(port=portname, baudrate=baudrate, 
            timeout=readTimeOut, write_timeout=writeTimeOut)

    def __str__(self) -> str:
        return self.portname

    def __del__(self):
        self.ser.close()
    
    def genCRC(self, input: bytes):
        # generate CRC as bytes type
        generator = 0x07
        crc = 0
        # mask is crutial to make crc uint8
        mask = 0xFF
        for byte in input:
            crc ^= byte
            crc &= mask
            for _ in range(8):
                if (crc & 0x80) != 0:
                    crc = ((crc << 1) & mask) ^ generator
                else:
                    crc = (crc << 1) & mask
        return bytes([crc & mask])

    def sendCommand(self, command: bytes, withCRC=False):
        # if withCRC, send an entra byte of CRC
        # return total number of bytes send        
        addr = command[0]
        rest = command[1:]
        numBytes = 0
        if withCRC:
            addr |= 1
        numBytes += self.ser.write(bytes([addr]))
        numBytes += self.ser.write(rest)
        if withCRC:
            crc = self.genCRC(bytes([addr]) + rest)
            numBytes += self.ser.write(crc)
        return numBytes

    def getResponse(self, maxLen: int):
        # clear input buffer when maxLen bytes are read
        response = self.ser.read(maxLen)
        self.ser.reset_input_buffer()
        return response

    def query(self, command: bytes, retLen, withCRC=False):
        # send command and get response
        for _ in range(3):
            # give 3 attemps
            self.sendCommand(command, withCRC)
            # test delay time later
            # depends on the platform
            # sleep(2 * (retLen / 8) + 1)
            response = self.getResponse(retLen)
            if len(response) == retLen:
                return response 
        return response

# give 3s for read or write timeout
Ser = serUtil('/dev/ttyUSB0', 612500, 3, 3)