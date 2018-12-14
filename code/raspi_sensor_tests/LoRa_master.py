import time
from SX127x.LoRa import *
#from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD

BOARD.setup()
BOARD.reset()
#parser = LoRaArgumentParser("Lora tester")


class mylora(LoRa):
    def __init__(self, verbose=False):
        super(mylora, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        self.var=0
        self.rcvd = ""
        self.last_rcvd_ID = 0
        self.stats = {"sent": 0, "rcvd": 0, "successRatio": "100%"}

    def on_rx_done(self):
        BOARD.led_on()
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        self.rcvd = bytes(payload[4:]).decode("utf-8")
        print("RX: {0}".format(self.rcvd))
        self.stats['rcvd'] += 1
        sr = round(self.stats['sent']/self.stats['rcvd'], 3)
        self.stats['successRatio'] = str(sr*100) + "%"
        print(self.stats)

        id_index = self.rcvd.find("ID: ")
        self.last_rcvd_ID = self.rcvd[id_index+5:id_index+8]
        BOARD.led_off()
        time.sleep(0.5)
        self.var=1

    def on_tx_done(self):
        print("\nTxDone")
        print(self.get_irq_flags())

    def on_cad_done(self):
        print("\non_CadDone")
        print(self.get_irq_flags())

    def on_rx_timeout(self):
        print("\non_RxTimeout")
        print(self.get_irq_flags())

    def on_valid_header(self):
        print("\non_ValidHeader")
        print(self.get_irq_flags())

    def on_payload_crc_error(self):
        print("\non_PayloadCrcError")
        print(self.get_irq_flags())

    def on_fhss_change_channel(self):
        print("\non_FhssChangeChannel")
        print(self.get_irq_flags())

    @staticmethod
    def utf8_packet(str):
        return (el.encode("utf-8") for el in str)

    def create_packet(self):
        p = ""
        p += "LastID: "
        p += str(self.last_rcvd_ID)
        p += "Sent: "
        p += str(self.stats['sent'])
        p += "Rcvd: "
        p += str(self.stats['rcvd'])
        p += "Succ: "
        p += self.stats['successRatio']
        return p

    def start(self):
        while True:
            while (self.var==0):
                #payload_str = self.create_packet()
                payload_str = "ABCDEFG"
                payload_b = list(bytearray(payload_str, "utf-8"))
                payload = [255, 255, 0, 0] + payload_b
                print("TX: {0}".format(payload_str))
                self.write_payload(payload) # Send INF
                self.set_mode(MODE.TX)
                self.stats['sent'] += 1
                time.sleep(2) # there must be a better solution but sleep() works
                self.reset_ptr_rx()
                self.set_mode(MODE.RXCONT) # Receiver mode
            
                start_time = time.time()
                while (time.time() - start_time < 3): # wait until receive data or 10s
                    pass;
            
            self.var=0
            self.reset_ptr_rx()
            self.set_mode(MODE.RXCONT) # Receiver mode
            time.sleep(3)

lora = mylora(verbose=False)
#args = parser.parse_args(lora) # configs in LoRaArgumentParser.py

#     Slow+long range  Bw = 125 kHz, Cr = 4/8, Sf = 4096chips/symbol, CRC on. 13 dBm
lora.set_pa_config(pa_select=1, max_power=21, output_power=17)
lora.set_bw(BW.BW125)
lora.set_coding_rate(CODING_RATE.CR4_8)
lora.set_spreading_factor(12)
lora.set_rx_crc(True)
#lora.set_implicit_header_mode(False)
#lora.set_lna_gain(GAIN.G1)
#lora.set_implicit_header_mode(False)
lora.set_low_data_rate_optim(True)

#  Medium Range  Defaults after init are 434.0MHz, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on 13 dBm
#lora.set_pa_config(pa_select=1)
print(lora.get_modem_config_1())

assert(lora.get_agc_auto_on() == 1)

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
