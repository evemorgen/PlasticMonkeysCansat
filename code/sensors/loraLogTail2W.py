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
        self.counter = 1
        self.tx_success = 1
        self.packet = ""
        self.payload_b = []
        self.tx_end = False

    def on_rx_done(self):
        self.clear_irq_flags(RxDone=1)
        raw_payload = self.read_payload(nocheck=True)
        payload = bytes(raw_payload).decode("utf-8",'ignore')
        
        rx_file = open("/home/pi/lora-logs/rx.txt", "a")
        rx_file.write(payload)
        rx_file.write("\n")
        rx_file.close()

        print ("Receive: " + payload)
        self.tx_success = 1
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

                temp_file = open("/home/pi/sensor_logs/bme_imu_temp.txt", "r")
                pres_file = open("/home/pi/sensor_logs/bme_imu_pres.txt", "r")
                temp_file.seek(0, 2)
                pres_file.seek(0, 2)
                t_len, p_len = temp_file.tell(), pres_file.tell()
                temp_file.seek(t_len-4, 0)
                pres_file.seek(p_len-4, 0)
                t = temp_file.read(3)
                p = pres_file.read(3)

                self.tx_success = 0
                self.packet = t+p
                #print(self.packet)
                payload_str = self.packet + "-"*(20-len(self.packet))
                payload_b = list(bytearray(payload_str, "utf-8"))
                #payload_b = self.payload_b
                payload = [255, 255, 0, 0] + payload_b
                
                print ("Send: " + payload_str)

                self.write_payload(payload)
                self.set_mode(MODE.TX)
                time.sleep(0.11) #TX time
                self.counter += 1
                self.reset_ptr_rx()
                self.set_mode(MODE.RXCONT) # Receiver mode
            
                start_time = time.time()
                while (time.time() - start_time < 0.17): # Slave responce
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

# Static text TX file
# tx_f = open("tx.txt", "r")

#Static binary TX file
#tx_f_bin = open("testimage_scaled.jpg", "rb")

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
