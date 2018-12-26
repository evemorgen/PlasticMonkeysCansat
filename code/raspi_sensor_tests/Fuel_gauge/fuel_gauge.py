from max1704x import MAX1704x
from time import sleep

fuel_gauge = MAX1704x()
print("Initial value: {}".format(fuel_gauge.get_soc()))

while True:
    soc = fuel_gauge.get_soc()
    v = fuel_gauge.get_voltage()/1000.0
    print("SOC: {:3s} Voltage: {:5.3f}mV".format(soc, v))
    sleep(30)
