import os
import time
import argparse
from pathlib import Path
from SX127x.LoRa import *
from SX127x.board_config import BOARD

HOME_PATH = Path.home()
RX_LOG = HOME_PATH / 'lora_logs' / 'rx.txt' #File, where all received data is stored
STATUS_LOG = HOME_PATH / 'lora_logs' / 'status.txt' #File, where this block's behavior is logged
CONF_FILE = HOME_PATH / 'lora_logs' / 'conf.txt' #File, where commands for this block are issued by other scripts

#Log files with data to be sent
#TODO: Argparse or .conf of some sort
TX_FILES = [
    HOME_PATH / 'sensor_logs' / 'alpha.txt',
    HOME_PATH / 'sensor_logs' / 'bravo.txt',
    HOME_PATH / 'sensor_logs' / 'charlie.txt'
]

IMAGES_PATH = HOME_PATH / 'images'
THERMAL_PATH = HOME_PATH / 'thermal'

UP_PACKET_LENGTH = 10 #Base -> Sat packet length in bytes
DOWN_PACKET_LENGTH = 25 #Sat -> Base packet length in bytes
CMD_LENGTH = 10

#DEFAULT transmission mode constants
MAX_BACKREAD = 5 #Maximal amount of lines expected to be logged into a file within one TX window
MAX_BUFFER_LENGTH = 50 #Maximal packet buffer length after which it overflows
MAX_BUFFER_APPEND = MAX_BACKREAD*len(TX_FILES)
TX_LINE_LENGTH = DOWN_PACKET_LENGTH-1 #TODO: Change this to match headers

TX_TIME = 0.11
RX_TIME = 0.17

class TXMODE:
    DEFAULT = 0
    IMAGE = 1
    THERMAL = 2


class HEADER: #Packet Headers
    MSGPACK = "M"
    IMAGE = "I"
    THERMAL = "T"
    STATUS = "S"


class myLoRa(LoRa):
    def __init__(self, verbose=False):
        super(myLoRa, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        self.tx_success = 1 #Keeps track of whether an ACK was rececived
        self.pending_packet = []
        self.tx_end = False #Set to true to stop the script
        self.tx_mode = TXMODE.DEFAULT
        self.filepos = {path: 0 for path in TX_FILES} #Tracks lengths of logfiles
        self.buffer = [] #Temporarily stores log readings to be sent


    def on_rx_done(self):
        self.clear_irq_flags(RxDone=1)
        raw_rx_payload = self.read_payload(nocheck=True) #
        payload = bytes(raw_payload).decode("utf-8", "ignore")
        with open(str(RX_LOG), "a") as rx_log:
            rx_log.write(payload)
            rx_log.write("-"*(UP_PACKET_LENGTH-len(payload)))
            rx_log.write("\n")
        print("RX: ", payload)
        self.tx_success=1


    def append_mgblk_buffer(self):
        if len(self.buffer) > MAX_BUFFER_LENGTH:
            print("Buffer overflow") 
            for _ in range(MAX_BUFFER_APPEND):
                self.buffer.pop(0) #Destroy enough data for the next reading to fit

        for path in TX_FILES:
            with open(str(path), 'r') as tx:
                tx.seek(0, 2)
                pos = tx.tell() #File length
                diff = round((pos-self.filepos[path])/25) #Amount of new readings
                self.filepos[path] = pos
                tx.seek(pos-MAX_BACKREAD*TX_LINE_LENGTH, 0)
                lines = [tx.read(TX_LINE_LENGTH) for i in range(MAX_BACKREAD)] #Read [MAX_BACKREAD] lines
            waiting = min(MAX_BACKREAD, diff)
            for i in range(MAX_BACKREAD-waiting, MAX_BACKREAD): #Append only the new ones to buffer
                self.buffer.append(lines[i])


    def tx_default(self):
        if len(self.buffer) == 0:
            print("Buffer empty!")
            return

        payload_str = HEADER.MSGPACK
        payload_str += self.buffer.pop(0) #
        payload_str += "-"*(25-len(payload_str))

        payload_b = list(bytearray(payload_str, "utf-8"))
        payload = [255, 255, 0, 0] + payload_b
        print("TX: " + payload_str)

        self.write_payload(payload)
        self.set_mode(MODE.TX)
        time.sleep(TX_TIME)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)


    def wait_for_rx(self):
        start_time = time.time()
        while time.time() - start_time < RX_TIME:
            pass
        self.reset_ptr_rx()


    def start(self):
        while True:
            #with open(CONF_FILE, "r") as conf:
            #    conf.seek(0, 2)
            #    conf.seek(conf.tell() - CMD_LENGTH, 0)
            #    cmd = conf.readLine()
            self.append_mgblk_buffer()
            self.tx_default()
            self.wait_for_rx()
            #print("######################")
            if self.tx_end:
                break


BOARD.setup()
BOARD.reset()

lora = myLoRa(verbose=False)
lora.set_freq(434.2)
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

