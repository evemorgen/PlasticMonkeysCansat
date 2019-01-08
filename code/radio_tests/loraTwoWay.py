import time
from SX127x.LoRa import *
from SX127x.board_config import BOARD

BOARD.setup()
BOARD.reset()


class mylora(LoRa):
    def __init__(self, verbose=False):
        super(mylora, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        self.var=0

    def on_rx_done(self):
        BOARD.led_on()
        self.clear_irq_flags(RxDone=1)
        raw_payload = self.read_payload(nocheck=True)
        payload = bytes(raw_payload).decode("utf-8",'ignore').strip('\x00')
        
        rx_file = open("rx.txt", "a")
        rx_file.write(payload)
        rx_file.write("\n")
        print ("Receive: " + payload)
        BOARD.led_off()
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

    def start(self):          
        while True:
            while (self.var==0):
                
                payload_str = "HelllllllooooooLORA"
                payload_b = list(bytearray(payload_str, "utf-8"))
                payload = [255, 255, 0, 0] + payload_b
                
                print ("Send: " + payload_str)

                self.write_payload(payload)
                self.set_mode(MODE.TX)
                time.sleep(0.2) #TX time
                self.reset_ptr_rx()
                self.set_mode(MODE.RXCONT) # Receiver mode
            
                start_time = time.time()
                while (time.time() - start_time < 0.3): # wait until receive data or 10s
                    pass;
            
            self.var=0
            self.reset_ptr_rx()

lora = mylora(verbose=False)
#args = parser.parse_args(lora) # configs in LoRaArgumentParser.py

#     Slow+long range  Bw = 125 kHz, Cr = 4/8, Sf = 4096chips/symbol, CRC on. 13 dBm
lora.set_freq(433.0)
lora.set_pa_config(pa_select=1, max_power=21, output_power=20)
lora.set_bw(BW.BW125)
lora.set_coding_rate(CODING_RATE.CR4_5)
lora.set_spreading_factor(7)
lora.set_preamble(12)
lora.set_rx_crc(True)
lora.set_low_data_rate_optim(False)

#  Medium Range  Defaults after init are 434.0MHz, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on 13 dBm
#lora.set_pa_config(pa_select=1)

#RX File
f = open("rx.txt", "w")
f.write("Hello")

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
