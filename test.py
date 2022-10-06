from batteryPack import batteryPack
from batteryModule import batteryModule

tesla = batteryPack()
tesla.reset()
tesla.clearFaults()

test = batteryModule()
test.readStatus()
