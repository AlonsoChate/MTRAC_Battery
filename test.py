from batteryCom import batteryModule
from serialUtility import serUtil


A = batteryModule()
A.readStatus()
print(A.alerts)
print(A.faults)
print(A.COVFaults)
print(A.CUVFaults)