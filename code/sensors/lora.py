import os
import time
import argparse
from pathlib import Path
from SX127x.LoRa import *
from SX127x.board_config import BOARD

HOME_PATH = Path.home()
LORA_LOGS = HOME_PATH / 'lora_logs'
RX_LOG = LORA_LOGS / 'rx.txt' #File, where all received data is stored
STATUS_LOG = LORA_LOGS / 'status.txt' #File, where this block's behavior is logged
CONF_FILE = LORA_LOGS / 'conf.txt' #File, where commands for this block are issued by other scripts
IMAGES = HOME_PATH / 'images'
THERMAL = HOME_PATH / 'thermal'

#Log files with data to be sent
#TODO: Argparse or .conf of some sort
TX_FILES = [
    HOME_PATH / 'sensor_logs' / 'alpha.txt',
    HOME_PATH / 'sensor_logs' / 'bravo.txt',
    HOME_PATH / 'sensor_logs' / 'charlie.txt'
]

IMAGES_PATH = HOME_PATH / 'images'
THERMAL_PATH = HOME_PATH / 'thermal'

UP_PACKET_LENGTH = 11 #Base -> Sat packet length in bytes
DOWN_PACKET_LENGTH = 25 #Sat -> Base packet length in bytes
CMD_LENGTH = 10

#DEFAULT transmission mode constants
MAX_BACKREAD = 5 #Maximal amount of lines expected to be logged into a file within one TX window
MAX_BUFFER_LENGTH = 50 #Maximal packet buffer length after which it overflows
MAX_BUFFER_APPEND = MAX_BACKREAD*len(TX_FILES)
TX_LINE_LENGTH = DOWN_PACKET_LENGTH-1

TX_TIME = 0.11
RX_TIME = 0.14

THERMAL_HEIGHT = 32
THERMAL_WIDTH = 24

IMG_QUAL = {
    'L': 'low',
    'M': 'medium',
    'H': 'high',
    'U': 'ultra'
}


class HEADER: #Packet Headers
    MSGPACK = "M"
    IMAGE = "I"
    THERMAL = "T"
    STATUS = "S"
    MSGPACK_B = 77
    IMAGE_B = 73
    THERMAL_B = 84
    STATUS_B = 83
    LORA = [255, 255, 0, 0]


class myLoRa(LoRa):
    def __init__(self, verbose=False):
        super(myLoRa, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        self.ack = {'thermal': 1, 'image':1} #Keeps track of whether an ACK was rececived
        self.image_waiting = []
        self.thermal_waiting = []
        self.tx_end = False #Set to true to stop the script
        self.filepos = {path: 0 for path in TX_FILES} #Tracks lengths of logfiles
        self.conf_filepos = 0
        self.buffer = [] #Temporarily stores log readings to be sent
        self.sending_image = False
        self.sending_thermal = False
        self.thermal_counter = 0
        self.image_size = 0
        self.last_tx_mode = 'default'

        with open(CONF_FILE, 'w') as cf:
            cf.write("NULLCMD--\n")


    def on_rx_done(self):
        """
        Triggers automatically upon LoRa interrupting received packets.
        Reads the packet and logs it into a file.
        """

        self.clear_irq_flags(RxDone=1)
        raw_rx_payload = self.read_payload(nocheck=True) #TODO fix that crc bug or implement high-layer crc
        payload = bytes(raw_rx_payload).decode("utf-8", "ignore").strip('\x00')
        with open(RX_LOG, "a") as rx_log:
            rx_log.write(payload)
            rx_log.write("-"*(UP_PACKET_LENGTH-len(payload)))
            rx_log.write("\n")
        print("RX:", payload)
        self.ack[self.last_tx_mode] = True #Acknowledge the previous packet


    def append_mgblk_buffer(self):
        """
        Adds new entries of casual input logs to the buffer queue.
        In case of an overflow, destroyes some data at hte front of the buffer.
        """

        if len(self.buffer) > MAX_BUFFER_LENGTH:
            print("Buffer overflow")
            for _ in range(MAX_BUFFER_APPEND):
                self.buffer.pop(0) #Destroy enough data for the next reading to fit

        for path in TX_FILES:
            with open(path, 'r') as tx:
                tx.seek(0, 2)
                pos = tx.tell() #File length
                diff = round((pos-self.filepos[path])/25) #Amount of new readings
                self.filepos[path] = pos
                tx.seek(pos-MAX_BACKREAD*TX_LINE_LENGTH, 0)
                lines = [tx.read(TX_LINE_LENGTH) for i in range(MAX_BACKREAD)] #Read [MAX_BACKREAD] lines
            waiting = min(MAX_BACKREAD, diff)
            for i in range(MAX_BACKREAD-waiting, MAX_BACKREAD): #Append only the new ones to buffer
                self.buffer.append(HEADER.MSGPACK + lines[i])


    def tx_default(self):
        """
        Retrieves the first packet from the buffer
        and transmits it.
        """

        if len(self.buffer) == 0:
            print("Buffer empty!")
            return

        payload_str = self.buffer.pop(0)
        payload_str += "-"*(25-len(payload_str))

        payload_b = list(bytearray(payload_str, "utf-8"))
        payload = HEADER.LORA + payload_b
        print("TX: " + payload_str)

        self.write_payload(payload)
        self.set_mode(MODE.TX)
        time.sleep(TX_TIME)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        self.last_tx_mode = 'default'


    def tx_image(self):
        """
        Transmits a chunk of picamera image data.
        If no ACK was received, same payload is sent.
        Otherwise a new chunk is loaded.
        Upon reaching end of file, stops the transmission.
        """

        if self.ack['image']: #If ACK received, send next slice of data
            self.image_waiting = [HEADER.IMAGE_B] + list(self.image.read(DOWN_PACKET_LENGTH-1))
            if self.image_waiting == [HEADER.IMAGE_B]: #If EOF, end image transmission
                self.sending_image = False
                return

        self.ack['image'] = False
        packet_length = len(self.image_waiting)
        if packet_length < DOWN_PACKET_LENGTH:
            self.image_waiting += (DOWN_PACKET_LENGTH-packet_length)*[45]
        print("TX:", self.image_waiting)

        self.write_payload(HEADER.LORA + self.image_waiting)
        self.set_mode(MODE.TX)
        time.sleep(TX_TIME)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        self.last_tx_mode = 'image'


    def tx_thermal(self):
        """
        Transmits a chunk of MLX90640 thermal image.
        If no ACK was received, same payload is sent.
        Otherwise, a new chunk is loaded.
        Upon transmitting 32 lines, stops the transmission
        """
        #NOT TESTED YET

        if self.ack['thermal']:
            self.thermal_counter += 1
            if self.thermal_counter >= THERMAL_HEIGHT:
                self.sending_thermal = False
                return
            row = [int(i) for i in self.thermal[self.thermal_counter]]
            row[:] = [max(el, 0) if el < 255 else min(el, 255) for el in row]
            self.thermal_waiting = [HEADER.THERMAL_B] + row

        print(self.thermal_waiting)
        self.ack['thermal'] = False
        self.write_payload(HEADER.LORA + self.thermal_waiting)
        self.set_mode(MODE.TX)
        time.sleep(TX_TIME)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        self.last_tx_mode = 'thermal'


    def wait_for_rx(self):
        """
        Waits for slave responce.
        No sleep() because of expected RX callback
        """

        start_time = time.time()
        while time.time() - start_time < RX_TIME:
            pass
        self.reset_ptr_rx()


    def parse_cmd(self):
        """
        Starts / ends transmissions based on received command
        """

        with open(CONF_FILE, "r") as conf:
            conf.seek(0, 2)
            pos = conf.tell()
            if pos > self.conf_filepos:
                self.conf_filepos = pos
                conf.seek(pos - CMD_LENGTH, 0)
                self.cmd = conf.readline()
                print("CMD:", self.cmd)

                if self.cmd[0] == "I" and not self.sending_image:
                    img_path = str(IMAGES) + '/' + str(self.cmd[1:6]) + '_' + IMG_QUAL[self.cmd[6]] + '.jpg'
                    self.image = open(img_path, "rb")
                    self.image_size = int(os.path.getsize(img_path))
                    self.sending_image = True
                    self.buffer.insert(0, "SI" + str(self.image_size) + '_' + self.cmd[1:6] + (DOWN_PACKET_LENGTH - 14)*"-")

                if self.cmd[0] == "T" and not self.sending_thermal:
                    with open(str(THERMAL)+ '/' + str(self.cmd[1:6])+".txt", "r") as t:
                        #Sorry, too tempting...
                        self.thermal = [[int(val) for val in line] for line in [line[:-2].split(" ") for line in t.readlines()]]
                    self.sending_thermal = True
                    self.thermal_counter = 0
                    self.buffer.insert(0, "ST" + str(self.cmd[1:6]) + (DOWN_PACKET_LENGTH - 7)*"-")


    def start(self):
        """
        Main loop
        """

        while True:
            self.append_mgblk_buffer()
            self.parse_cmd()
            self.tx_default()
            self.wait_for_rx()
            if self.sending_image:
                self.tx_image()
                self.wait_for_rx()

            if self.sending_thermal:
                self.tx_thermal()
                self.wait_for_rx()

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

