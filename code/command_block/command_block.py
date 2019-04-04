import os
from time import sleep
import subprocess
import configparser

lastLine = None
sensor_logs = "foo"
sensors = "foo"

def image_request(line):
    camera_log = open(sensor_logs + "camera.txt")
    lora_status = open(sensor_logs + "lora_status.txt", "a")
    tstamps = camera_log.readlines()
    t = int(line[1:6])
    q = line[6]
    ti = min([abs(t-int(x)) for x in tstamps])
    tim = t - ti if str(t - ti)+"\n" in tstamps else t + ti
    lora_status.write("I " + str(tim) + " " + str(q) + '\n')
    lora_status.close()

def thermal_request(line):
    thermal_log = open(sensor_logs + "thermal.txt")
    lora_status = open(sensor_logs + "lora_status.txt", "a")
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
    lora_status = open(sensor_logs + "lora_status.txt", "a")
    lora_status.write("S 0 0")
    lora_status.close()

def print_text(line):
    t = line[1]
    cmd = "python3 " + sensors+"oled.py " + str(t)
    subprocess.Popen(cmd)

def print_system_info_oled():
    cmd = "python3 " + sensors+"oled.py S"
    subprocess.Popen(cmd)

while True:
    rx_f = open("foo/rx.txt", "r")
    rx_f.seek(0,2)
    rx_f.seek(rx_f.tell()-26, 0)
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
    if line[0] == "P":
        print_text(line)
    if line[0] == "H":
        print_system_info_oled()
    sleep(0.1)
