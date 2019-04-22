##############################
# WORKS ONLY WITH PYTHON 3.7 #
##############################

import os
import time
import configparser
from pathlib import Path
from SX127x.LoRa import *
from SX127x.board_config import BOARD

cparser = configparser.ConfigParser()
cparser.read('config.ini')

RX_LOG = Path(cparser['util']['rx_log']) #File, where all received data is stored
STATUS_LOG = Path(cparser['util']['status_log']) #File, where this block's behavior is logged
CMD_FILE = Path(cparser['util']['cmd_file']) #File, where commands for this block are issued by other scripts
IMAGES = Path(cparser['util']['images'])
THERMAL = Path(cparser['util']['thermal'])

#Log files with data to be sent
TX_FILES = [Path(p) for p in cparser['data'].values()]

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
        super().__init__(verbose)
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

        with open(CMD_FILE, 'w') as cf:
            cf.write("NULLCMD--\n") #write some characters to prevent negative seek()


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

    def send(self, payload):
        """
        Writes the given payload to LoRa module, while taking care
        of all technical issues.
        :param payload: payload to be written
        """

        self.write_payload(HEADER.LORA + payload)
        self.set_mode(MODE.TX)
        time.sleep(TX_TIME)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)


    def append_mgblk_buffer(self, line_length, raw=False):
        """
        Adds new entries of casual input logs to the buffer queue.
        In case of an overflow, destroyes some data at hte front of the buffer.
        """

        if len(self.buffer) > MAX_BUFFER_LENGTH:
            print("Buffer overflow")
            for _ in range(MAX_BUFFER_APPEND):
                self.buffer.pop(0) #Destroy enough data for the next reading to fit

        for path in TX_FILES:
            with open(path, 'rb') as tx:
                tx.seek(0, 2)
                pos = tx.tell() #File length
                diff = round((pos-self.filepos[path])/line_length) #Amount of new readings
                self.filepos[path] = pos
                tx.seek(pos-MAX_BACKREAD*line_length, 0)
                raw_lines = [list(tx.read(line_length)) for i in range(MAX_BACKREAD)] #Read [MAX_BACKREAD] lines
                parsed_lines = [line[:line[0]+1] for line in raw_lines]  #Remove mergeblock wrappers

            waiting = min(MAX_BACKREAD, diff)
            for i in range(MAX_BACKREAD-waiting, MAX_BACKREAD): #Append only the new ones to buffer
                self.buffer.append([HEADER.MSGPACK_B] + (raw_lines[i] if raw else parsed_lines[i]))


    def tx_default(self):
        """
        Retrieves the first packet from the buffer
        and transmits it.
        """

        if len(self.buffer) == 0:
            print("Buffer empty!")
            self.buffer.insert(0, "SSBuffer Empty!")

        payload = self.buffer.pop(0)
        if type(payload) is str:
            payload += "-"*(DOWN_PACKET_LENGTH-len(payload))
            payload = list(bytearray(payload, "utf-8"))
        elif type(payload) is list:
            payload += [45]*(DOWN_PACKET_LENGTH-len(payload))
        print("TX:", payload)

        assert(len(payload) == DOWN_PACKET_LENGTH)
        self.send(payload)
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

        self.send(self.image_waiting)
        self.last_tx_mode = 'image'


    def tx_thermal(self):
        """
        Transmits a chunk of MLX90640 thermal image.
        If no ACK was received, same payload is sent.
        Otherwise, a new chunk is loaded.
        Upon transmitting 32 lines, stops the transmission
        """

        if self.ack['thermal']:
            self.thermal_counter += 1
            if self.thermal_counter > THERMAL_HEIGHT:
                self.sending_thermal = False
                return
            row = [int(i) for i in self.thermal[self.thermal_counter-1]]
            row[:] = [max(el, 0) if el < 255 else min(el, 255) for el in row]
            self.thermal_waiting = [HEADER.THERMAL_B] + row

        print(self.thermal_waiting)
        self.ack['thermal'] = False
        self.send(self.thermal_waiting)
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

        with open(CMD_FILE, "r") as conf:
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
                    self.buffer.insert(0, "SI{:07}".format(self.image_size) + self.cmd[1:7] + (DOWN_PACKET_LENGTH - 13)*"-")

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
            self.append_mgblk_buffer(30, False)
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

lora.start()
