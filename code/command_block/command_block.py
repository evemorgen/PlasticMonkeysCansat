import os
from time import sleep
import subprocess
import configparser

lastLine = None
sensor_logs = "foo"
text_buffer = "buffer.txt"
lora_status_file = "lora_status.txt"
rx_file = "foo/rx.txt"

def image_request(line):
    camera_log = open(sensor_logs + "camera.txt")
    lora_status = open(lora_status_file, "a")
    tstamps = camera_log.readlines()
    t = int(line[1:6])
    q = line[6]
    ti = min([abs(t-int(x)) for x in tstamps])
    tim = t - ti if str(t - ti)+"\n" in tstamps else t + ti
    lora_status.write("I " + str(tim) + " " + str(q) + '\n')
    lora_status.close()

def thermal_request(line):
    thermal_log = open(sensor_logs + "thermal.txt")
    lora_status = open(lora_status_file, "a")
    tstamps = thermal_log.readlines()
    t = int(line[1:6])
    ti = min([abs(t-int(x)) for x in tstamps])
    tim = t - ti if str(t - ti)+"\n" in tstamps else t + ti
    lora_status.write("T " + str(tim) + " " + 0 + '\n')
    lora_status.close()

def system_reboot():
    cmd = "reboot"
    print("rebooting")
    subprocess.Popen(cmd)

def send_system_info():
    lora_status = open(lora_status_file, "a")
    lora_status.write("S 0 0")
    lora_status.close()

def append_text(line):
    text = str(line[1:10])
    buffer = open(text_buffer, "a")
    buffer.write(text)

def clear_buffer():
    open(text_buffer,'w').close()

while True:
    rx_f = open(rx_file, "r")
    rx_f.seek(0,2)
    rx_f.seek(rx_f.tell()-12, 0) #Packet should have a size of 11 - header + 10 characters
    line = rx_f.readline().strip("\x00")
    rx_f.close()
    print(line)
    if line[0] == "I":
        image_request(line)
    if line[0] == "T":
        thermal_request(line)
    if line[0] == "R":
        system_reboot()
    if line[0] == "S":
        send_system_info()
    if line[0] == "A":
        append_text(line)
    if line[0] == "C":
        clear_buffer()
    sleep(0.1)
