from time import sleep
from serial import Serial

# to make pyserial work, either give read and write permission to the virtual driver
# or add current user to group dialout
# $sudo usermod -a -G dialout <username>

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
                    crc = (crc << 1) & mask ^ generator
                else:
                    crc = crc << 1 & mask
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
            crc = self.genCRC(command)
            numBytes += self.ser.write(crc)
        return numBytes

    def getResponse(self, maxLen: int):
        # clear input buffer when maxLen bytes are read
        response = self.ser.read(maxLen)
        self.ser.reset_input_buffer()
        return response

    def query(self, command: bytes, retLen, withCRC=False):
        # send command and get response
        for _ in range(5):
            # give 5 attemps
            self.sendCommand(command, withCRC)
            # TODO test delay time later
            # sleep(2 * (retLen / 8) + 1)
            response = self.getResponse(retLen)
            if len(response) == retLen:
                return response 
        return response