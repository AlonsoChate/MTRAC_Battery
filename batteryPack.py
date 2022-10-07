from batteryModule import batteryModule
from serialUtility import Ser, inst

class batteryPack:
    def __init__(self):
        self.modules = []
        self.reset()        # reset all address
        self.setBoardAddr() # set sequential addr
        self.clearFaults()  # clear faults by reset

    def reset(self):
        # broadcast to set the address of all boards to 0
        # and then assign address start from 1
        command = bytes([0x3F << 1]) + bytes([0x3C]) + bytes([0xA5])
        for _ in range(3): # give 3 attemps
            response = Ser.query(command, 4, True)
            if response[0]==0x7F and response[1]==0x3c and response[2]==0xa5:
                print("Reset successful")
                break

    def setBoardAddr(self):
        # set the address of board (start from 1) after reset()
        # basically query address 0 and then set the address 
        # if send a command to address 0 and no one responds then every board is inialized
        # will spend some time when there's no response (every board is set)
        index = 1 # start assign from 1
        while True:
            command = bytes([0]) + bytes([0]) + bytes([1])
            response = Ser.query(command, 4, False)
            if len(response) == 4:
                # there's board with address 0
                if response[0]==0x80 and response[1]==0 and response[2]==1:
                    print("Response of address 0")
                    command = bytes([0]) + bytes([inst['REG_ADDR_CTRL']]) + bytes([index + 0x80])
                    response = Ser.query(command, 4, True)
                    # check response
                    if response[0]==0x81 and response[1]==inst['REG_ADDR_CTRL'] and response[2]==(index+0x80):
                        temp = batteryModule()
                        temp.moduleAddr = index
                        self.modules.append(temp)
                        print("Address %d set" % index)
                        index += 1
            else:
                # every board is set
                print("setBoard: all boards set")
                return

    def clearFaults(self):
        # broadcast to clear the faults and alerts caused by reset
        field0 = 0x7f                       # broadcast
        field1 = inst['REG_ALERT_STATUS']   # alert status
        field2 = 0xff                       # cause reset
        command = bytes([field0]) + bytes([field1]) + bytes([field2])
        Ser.query(command, 4, True) 

        field2 = 0x00                       # write 0 to register
        command = bytes([field0]) + bytes([field1]) + bytes([field2])
        Ser.query(command, 4, True) 

        field0 = 0x7f                       # broadcast
        field1 = inst['REG_FAULT_STATUS']   # fault status
        field2 = 0xff;                       # cause reset
        command = bytes([field0]) + bytes([field1]) + bytes([field2])
        Ser.query(command, 4, True) 

        field2 = 0x00                       # write 0 to register
        command = bytes([field0]) + bytes([field1]) + bytes([field2])
        Ser.query(command, 4, True) 

        print("Clear faults")