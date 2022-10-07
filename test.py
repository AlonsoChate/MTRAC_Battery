from batteryPack import batteryPack
from batteryModule import batteryModule

tesla = batteryPack()
tesla.reset()
tesla.clearFaults()


mod : batteryModule = tesla.modules[0]

mod.readStatus()

mod.readValues()

pass