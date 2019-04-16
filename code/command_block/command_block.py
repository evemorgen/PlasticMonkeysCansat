from time import sleep
import subprocess
import os

sensor_logs = "foo"
text_buffer = "buffer.txt"
lora_status_file = "lora_status.txt"
rx_file = "foo/rx.txt"
file_size = None

def image_request(line):
    camera_log = open(sensor_logs + "camera.txt")
    lora_status = open(lora_status_file, "a")
    tstamps = camera_log.readlines()
    t = int(line[1:6])
    q = line[6]
    ti = min([abs(t-int(x)) for x in tstamps])
    tim = t - ti if str(t - ti)+"\n" in tstamps else t + ti
    lora_status.write("I{:05}{}---\n".format(tim, q))
    lora_status.close()

def thermal_request(line):
    thermal_log = open(sensor_logs + "thermal.txt")
    lora_status = open(lora_status_file, "a")
    tstamps = thermal_log.readlines()
    t = int(line[1:6])
    ti = min([abs(t-int(x)) for x in tstamps])
    tim = t - ti if str(t - ti)+"\n" in tstamps else t + ti
    lora_status.write("T{:05}----\n".format(tim))
    lora_status.close()

def system_reboot(line):
    if str(line[0:5]) == "REBOOT":
        cmd = "reboot"
        subprocess.Popen(cmd)

def send_system_info(line):
    lora_status = open(lora_status_file, "a")
    lora_status.write("S{:09}\n".format(0))
    lora_status.close()

def append_text(line):
    text = str(line[1:10])
    buffer = open(text_buffer, "a")
    buffer.write(text)

def clear_buffer(line):
    open(text_buffer,'w').close()

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
        rx_f = open(rx_file, "r")
        new_size = os.stat(rx_file).st_size
        if file_size != new_size: #prevents from getting the same command multiple time
            file_size = new_size
            rx_f.seek(0,2)
            rx_f.seek(rx_f.tell()-12, 0) #Packet should have a size of 11 - header + 10 characters
            line = rx_f.readline()
            rx_f.close()
            command_dict[line[0]](line) #runs a certain command from dict
        sleep(0.03)
    except Exception: #to prevent program from crashing when the header does not exist in dict
        sleep(0.03)
