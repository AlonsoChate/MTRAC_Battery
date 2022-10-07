from batteryPack import batteryPack
from batteryModule import batteryModule

tesla = batteryPack()
module:batteryModule = tesla.modules[0]
module.update()

# print output
print("Status:")
print("     alert:      %d" % module.alerts)
print("     faults:     %d" % module.faults)
print("     COVFaults:  %d" % module.COVFaults)
print("     CUVFaults:  %d" % module.CUVFaults)
print("Voltages & Temperatures:")
print("     module vol: %fV" % module.moduleVolt)
print("     temp0:      %f" % module.temperature[0])
print("     temp1:      %f" % module.temperature[1])
print("Cell voltages:")
print("     cell0:      %fV" % module.cellVolt[0])
print("     cell1:      %fV" % module.cellVolt[1])
print("     cell2:      %fV" % module.cellVolt[2])
print("     cell3:      %fV" % module.cellVolt[3])
print("     cell4:      %fV" % module.cellVolt[4])
print("     cell5:      %fV" % module.cellVolt[5])