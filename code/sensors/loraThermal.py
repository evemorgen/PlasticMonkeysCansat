import sys
import os
import time
from SX127x.LoRa import *
from SX127x.board_config import BOARD

BOARD.setup()
BOARD.reset()

image_path = sys.argv[1]
image_size = int(os.path.getsize(image_path))
print("\nSENDING THERMAL: " + str(image_path) + " of " + str(image_size) + " bytes\n")

thermal_file = open(image_path)
thermal = [thermal_file.readline()[:-1].split() for i in range(32)]


class mylora(LoRa):
    def __init__(self, verbose=False):
        super(mylora, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        self.var=0
        self.counter = 1
        self.tx_success = 0
        self.packet = ""
        self.payload_b = []
        self.tx_end = False
        self.sent_counter = 0


    def on_rx_done(self):
        self.clear_irq_flags(RxDone=1)
        raw_payload = self.read_payload(nocheck=True)
        payload = bytes(raw_payload).decode("utf-8",'ignore').strip("\x00")

        rx_file = open("/home/pi/lora-logs/rx.txt", "a")
        rx_file.write(payload)
        rx_file.write("\n")
        rx_file.close()

        print ("Receive: " + payload)
        self.tx_success = 1
        self.var=1


    def start(self):
        p = "T"
        self.payload_b = list(bytearray(p, "utf-8"))
        while True:
            while (self.var==0):

                if self.tx_success:
                    self.sent_counter += 1
                    if self.sent_counter >= 32:
                        self.tx_end = True
                        break
                    self.payload_b = [int(i) - 100 for i in thermal[self.sent_counter]]
                self.tx_success = 0
                if len(self.payload_b) < 25:
                    self.payload_b += (25-len(self.payload_b))*[45]
                    print("Modified payload: ", self.payload_b)
                print(self.payload_b)
                payload_b = self.payload_b
                payload = [255, 255, 0, 0] + payload_b
                
                self.write_payload(payload)
                self.set_mode(MODE.TX)
                time.sleep(0.11) #TX time
                self.counter += 1
                self.reset_ptr_rx()
                self.set_mode(MODE.RXCONT) # Receiver mode
            
                start_time = time.time()
                while (time.time() - start_time < 0.11): # Slave responce
                    pass;
            
            self.var=0
            self.reset_ptr_rx()
            if self.tx_end:
                break

lora = mylora(verbose=False)
lora.set_freq(433.0)
lora.set_pa_config(pa_select=1, max_power=21, output_power=20)
lora.set_bw(BW.BW125)
lora.set_coding_rate(CODING_RATE.CR4_5)
lora.set_spreading_factor(7)
lora.set_preamble(12)
lora.set_rx_crc(True)
lora.set_low_data_rate_optim(False)

assert(lora.get_agc_auto_on() == 1)

try:
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    sys.stderr.write("KeyboardInterrupt\n")
finally:
    sys.stdout.flush()
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
