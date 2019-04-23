from time import sleep
import subprocess
import configparser
import sys
import os

config_file = sys.argv[1]
config = configparser.ConfigParser()
config.read(config_file)

CAMERA_LOGS = config['SETTINGS']['camera_log_file']
THERMAL_LOGS = config['SETTINGS']['thermal_log_file']
TEXT_BUFFER = config['SETTINGS']['oled_text_buffer']
LORA_STATUS_FILE = config['SETTINGS']['lora_status_file']
RX_FILE = config['SETTINGS']['rx_file']
SLEEP_TIME = float(config['SETTINGS']['sleep_time'])
EXCEPTION_SLEEP_TIME = float(config['SETTINGS']['exception_sleep_time'])
LINE_LENGTH = int(config['SETTINGS']['packet_line_length']) #number of characters in packet, 7 is minimum
TIMESTAMP_LENGTH =  int(config['SETTINGS']['timestamp_length']) #number of characters defining timestamp in packet
file_size = None

def image_request(line):
    camera_log = open(CAMERA_LOGS)
    lora_status = open(LORA_STATUS_FILE, "a")
    tstamps = camera_log.readlines()
    t = int(line[1:(TIMESTAMP_LENGTH+1)])
    q = line[6]
    ti = min([abs(t-int(x)) for x in tstamps])
    tim = t - ti if str(t - ti)+"\n" in tstamps else t + ti
    lora_status.write("I{:05}{}---\n".format(tim, q))
    lora_status.close()

def thermal_request(line):
    thermal_log = open(THERMAL_LOGS)
    lora_status = open(LORA_STATUS_FILE, "a")
    tstamps = thermal_log.readlines()
    t = int(line[1:(TIMESTAMP_LENGTH+1)])
    ti = min([abs(t-int(x)) for x in tstamps])
    tim = t - ti if str(t - ti)+"\n" in tstamps else t + ti
    lora_status.write("T{:05}----\n".format(tim))
    lora_status.close()

def system_reboot(line):
    if str(line[0:6]) == "REBOOT":
        cmd = "reboot"
        subprocess.Popen(cmd)

def send_system_info(line):
    lora_status = open(LORA_STATUS_FILE, "a")
    lora_status.write("S{:09}\n".format(0))
    lora_status.close()

def append_text(line):
    text = str(line[1:(LINE_LENGTH)])
    buffer = open(TEXT_BUFFER, "a")
    buffer.write(text)

def clear_buffer(line):
    open(TEXT_BUFFER,'w').close()

command_dict = {
    "I": image_request,
    "T": thermal_request,
    "R": system_reboot,
    "S": send_system_info,
    "A": append_text,
    "C": clear_buffer,
}

while True:
    try:
        rx_f = open(RX_FILE, "r")
        new_size = os.stat(RX_FILE).st_size
        if file_size != new_size: #prevents from getting the same command multiple time
            file_size = new_size
            rx_f.seek(0,2)
            rx_f.seek(rx_f.tell()-(LINE_LENGTH+1), 0) #Packet should have a size of 11 - header + 10 characters
            line = rx_f.readline()
            rx_f.close()
            command_dict[line[0]](line) #runs a certain command from dict
        sleep(SLEEP_TIME)
    except Exception: #to prevent program from crashing when the header does not exist in dict
        sleep(EXCEPTION_SLEEP_TIME)
