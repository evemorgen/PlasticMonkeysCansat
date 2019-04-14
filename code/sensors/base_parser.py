from __future__ import print_function
import struct
import serial
import sys
from time import time
from pathlib import Path

UP_PACKET_LENGTH = 11
DOWN_PACKET_LENGTH = 25

MAX_TX_BUFFER_LENGTH = 10
MAX_BACKREAD = 6

THERMAL_HEIGHT = 32

HEADERS = {
    'S': "status",
    'I': "image_get",
    'T': "thermal_get",
    'M': "default"
}

STATUS_HEADERS = {
    'I': "image_init",
    'T': "thermal_init",
    'E': "error",
    'S': "system"
}


class rxParser:
    def __init__(self, port, baudrate, images_path, thermal_path, tx_path, rx_file):
        self.ser = serial.Serial(port, baudrate)
        self.images_path = images_path
        self.thermal_path = thermal_path
        self.tx_path = tx_path
        self.rx_file = rx_file
        self.tx_file_pos = 0
        self.image = None
        self.image_size = 0
        self.img_rcvd_bytes = 0
        self.lastTX = None
        self.img_lastline = None
        self.thermal_lastline = None
        self.thermal_counter = 0
        self.line = None
        self.tx_buffer = []

        with open(self.tx_path, "w") as tx:
            tx.write("0"*MAX_BACKREAD*UP_PACKET_LENGTH)


    def image_init(self):
        print("RECEIVING IMAGE", self.line[:15])
        self.image = open(self.images_path+''.join(self.line[9:15])+"_"+str(time())+".jpg", "wb")
        self.image_size = int("".join(self.line[2:9]))
        self.img_rcvd_bytes = 0


    def image_get(self):
        img_line = self.line[1:]
        if img_line != self.img_lastline:
            self.img_rcvd_bytes += DOWN_PACKET_LENGTH-1
            print("I", img_line)
            if self.img_rcvd_bytes > self.image_size:
                self.image.write(bytes(img_line[:(self.img_rcvd_bytes-self.image_size)]))
                self.image.close()
            else:
                self.image.write(bytes("".join(img_line)))
        self.img_lastline = img_line


    def thermal_init(self):
        print("RECEIVING THERMAL", self.line[:15])
        self.thermal = open(self.thermal_path+''.join(self.line[2:7])+"_"+str(time())+".txt", "w")
        self.thermal_counter = 0


    def thermal_get(self):
        thermal_line = self.line[1:]
        if thermal_line != self.thermal_lastline:
            self.thermal_counter += 1
            print(self.thermal_counter)
            print("T", thermal_line)
            parsed_line = ["%.1f"%(ord(el)/10.0) for el in thermal_line]
            self.thermal.write(" ".join(parsed_line))
            self.thermal.write('\n')

        self.thermal_lastline = thermal_line
        if self.thermal_counter == THERMAL_HEIGHT:
            self.thermal.close()

    def system(self):
        print("System: ", "".join(self.line[2:]).strip('-'))

    def status(self):
        getattr(self, STATUS_HEADERS[self.line[1]])()


    def default(self):
        pack = "".join(self.line[1:])
        print("M:", pack)
        with open(self.rx_file, "ab") as rf:
            rf.write(pack)


    def tx(self):
        if len(self.tx_buffer) > MAX_TX_BUFFER_LENGTH:
            print("TxBufferOverflow: buffer cleared")
            self.tx_buffer = []

        with open(self.tx_path, "r") as tx:
            tx.seek(0, 2)
            pos = tx.tell()
            diff = int(((pos-self.tx_file_pos)/UP_PACKET_LENGTH))
            self.tx_file_pos = pos
            tx.seek(pos-MAX_BACKREAD*UP_PACKET_LENGTH, 0)
            lines = [tx.read(UP_PACKET_LENGTH) for _ in range(MAX_BACKREAD)]
        waiting = min(MAX_BACKREAD, diff)
        for i in range(MAX_BACKREAD-waiting, MAX_BACKREAD):
            self.tx_buffer.append(lines[i].strip("-"))

        if len(self.tx_buffer) == 0:
            #print("Buffer empty!")
            return

        payload = self.tx_buffer.pop(0)
        print("TX:", payload)
        self.ser.write(payload)

    def start(self):
        while True:
            if self.ser.in_waiting >= 0:
                self.line = list(self.ser.read(DOWN_PACKET_LENGTH))
                getattr(self, HEADERS[self.line[0]])()
                self.tx()

rxparser = rxParser("/dev/ttyUSB0", 9600, "../../../images/", "../../../thermal/", "../../../tx.txt", "../../../rx.txt")
rxparser.start()

