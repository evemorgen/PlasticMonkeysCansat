import time
import argparse
from SX127x.LoRa import *
#from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD

BOARD.setup()
BOARD.reset()
#parser = LoRaArgumentParser("Lora tester")


class mylora(LoRa):
    def __init__(self, verbose=False, delay=1, length=50):
        super(mylora, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        self.var=0
        self.rcvd = ""
        self.last_rcvd_ID = 0
        self.length = length
        self.delay = delay
        self.stats = {"sent": 0, "rcvd": 0, "successRatio": "100%", "last_sent": 0}

    def on_rx_done(self):
        """
        BOARD.led_on()
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        self.rcvd = bytes(payload[4:]).decode("utf-8")
        print("RX: {0}".format(self.rcvd))
        self.stats['rcvd'] += 1
        sr = round(self.stats['rcvd']/self.stats['sent'], 4)
        self.stats['successRatio'] = str(sr*100) + "%"
        print(self.stats)

        id_index = self.rcvd.find("ID: ")
        self.last_rcvd_ID = self.rcvd[id_index+5:id_index+8]
        time.sleep(0.5)
        BOARD.led_off()
        """
        self.var=1

    @staticmethod
    def utf8_packet(str):
        return (el.encode("utf-8") for el in str)

    def start(self):
        print(self.length, self.delay)
        while True:
            while (self.var==0):

                payload_str = str(self.stats['sent']) + "A" * self.length
                payload_b = list(bytearray(payload_str, "utf-8"))
                payload = [255, 255, 0, 0] + payload_b
                self.write_payload(payload) # Send INF
                self.set_mode(MODE.TX)
                self.stats['sent'] += 1
                self.stats['last_sent'] = time.time()
                self.stats['payload_len'] = len(payload_str)
                print(self.stats)
                time.sleep(self.delay) # there must be a better solution but sleep() works
                #aself.reset_ptr_rx()
                #self.set_mode(MODE.RXCONT) # Receiver mode
            
                #start_time = time.time()
                #while (time.time() - start_time < 3): # wait until receive data or 10s
                #    pass
            
            #self.var=0
            #self.reset_ptr_rx()
            #self.set_mode(MODE.RXCONT) # Receiver mode
            #time.sleep(0.9)


parser = argparse.ArgumentParser(description='LoRa range tests script #1')
parser.add_argument('--spread-factor', '-sf', help='spreading factor number', type=int, default=8)
parser.add_argument('--coding-rate', '-cr', help='coding rate denominatior', type=int, default=5)
parser.add_argument('--delay', '-d', help='delay between packets send', type=float)
parser.add_argument('--packet-length', '-l', help='number of bytes to send in one packet', type=int)
args = parser.parse_args()
print(args)

lora = mylora(verbose=False, delay=args.delay, length=args.packet_length)
#args = parser.parse_args(lora) # configs in LoRaArgumentParser.py

lora.set_freq(433.0)
#     Slow+long range  Bw = 125 kHz, Cr = 4/8, Sf = 4096chips/symbol, CRC on. 13 dBm
lora.set_pa_config(pa_select=1, max_power=21, output_power=17)
lora.set_bw(BW.BW125)
cr_dict = {
    5: CODING_RATE.CR4_5,        
    6: CODING_RATE.CR4_6,
    7: CODING_RATE.CR4_7,        
    8: CODING_RATE.CR4_8        
}
lora.set_coding_rate(cr_dict[args.coding_rate])
lora.set_spreading_factor(args.spread_factor)
lora.set_rx_crc(True)
lora.set_preamble(12)
#lora.set_implicit_header_mode(False)
#lora.set_lna_gain(GAIN.G1)

#FIXME For sf lower than 11 set to FALSE 
lora.set_low_data_rate_optim(False)

#  Medium Range  Defaults after init are 434.0MHz, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on 13 dBm
#lora.set_pa_config(pa_select=1)
print(lora.get_modem_config_1())
print("Preamble: {0}".format(lora.get_preamble()))
assert(lora.get_agc_auto_on() == 1)

print(lora.get_all_registers())

try:
    print("START")
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("Exit")
    sys.stderr.write("KeyboardInterrupt\n")
finally:
    sys.stdout.flush()
    print("Exit")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
