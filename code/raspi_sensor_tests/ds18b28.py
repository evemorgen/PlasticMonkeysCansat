from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor()
t = sensor.get_temperature()
print("DS18B20 Temp: {0:.1f}\n".format(t))
