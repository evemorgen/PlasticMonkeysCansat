from smbus import SMBus

class MAX1704x(object):
    VERSION_LOW_REG  = 0x09
    VOLTAGE_HIGH_REG = 0x02
    VOLTAGE_LOW_REG  = 0x03
    SOC_HIGH_REG     = 0x04
    SOC_LOW_REG      = 0x05
    CONFIG_HIGH_REG  = 0x0C
    CONFIG_LOW_REG   = 0x0D
    CONFIG_ALARM_BIT = 5
    CONFIG_SLEEP_BIT = 7

    voltage_coeffs = {3:1.25, 4:2.5}
    
    def __init__(self, bus=1, addr=0x36):
        self.bus_num = bus
        self.bus = SMBus(self.bus_num)
        self.addr = addr
        self.version = self.bus.read_byte_data(self.addr, self.VERSION_LOW_REG)
        
    def get_voltage(self):
        high = self.bus.read_byte_data(self.addr, self.VOLTAGE_HIGH_REG)
        low = self.bus.read_byte_data(self.addr, self.VOLTAGE_LOW_REG)
        result = ((high<<4) + (low>>4)) * self.voltage_coeffs[self.version]
        return result

    def get_soc(self):
        percents = self.bus.read_byte_data(self.addr, self.SOC_HIGH_REG)
        result = "{}%".format(percents)
        return result

    def alarm_occured(self):
        status = self.bus.read_byte_data(self.addr, self.CONFIG_LOW_REG)
        return status & 1<<self.CONFIG_ALARM_BIT


if __name__ == "__main__":
    max1704x = MAX1704x()
    print(max1704x.get_voltage())
    print(max1704x.get_soc())
    print("Alarm status: {}".format(bool(max1704x.alarm_occured())))
