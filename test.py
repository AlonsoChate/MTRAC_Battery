from batteryCom import batteryModule
from serialUtility import serUtil


# test = serUtil('/dev/ttyUSB0', 612500, 5, 5)
# command = bytes([(0x3F << 1) | 1])+bytes([0x3C])+bytes([0xA5])
# a = test.genCRC(command)
# print(hex(int.from_bytes(a, 'big')))
# test.sendCommand(command, True)
# test.sendCommand(command)
# response = test.getResponse(8)
# print(len(response))
# for i in response:
#     print(hex(i))
# pass

A = batteryModule()
A.reset()
A.readStatus()
print(A.alerts)
A.readValues()
