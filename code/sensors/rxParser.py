
import os
from time import sleep
import subprocess

lastLine = None
sensor_logs = "/home/pi/sensor_logs/"
images = "/home/pi/images/"
sensors = "/home/pi/PlasticMonkeysCanSat/code/sensors/"

qual = {
    'L': 'low',
    'M': 'medium',
    'H': 'high',
    'R': 'raw',
    'U': 'ultra'
}

def kill_lora():
    pid = int(open("/home/pi/lora_logs/sys.txt", "r").readline())
    try:
        os.system("kill "+str(pid))
    except Exception:
        pass


while True:
    rx_f = open("/home/pi/lora_logs/rx.txt", "r")
    rx_f.seek(0,2)
    rx_f.seek(rx_f.tell()-26, 0)
    line = rx_f.readline().strip("\x00")
    rx_f.close()
    #print(line)
    if line[0] == "I":
        camera_log = open(sensor_logs + "camera.txt")
        tstamps = camera_log.readlines()
        t = int(line[1:6])
        q = line[6]
        ti = min([abs(t-int(x)) for x in tstamps])
        tim = t - ti if str(t - ti)+"\n" in tstamps else t + ti
        print(t, ti, tim)
        print(tstamps)
        kill_lora()
        cmd = "python3 " + sensors+"loraImage.py " + images+str(tim)+"_"+qual[q]+".jpg"
        print(cmd)
        subprocess.Popen(cmd.split()).wait()
        print("Image transmission complete")
        sleep(1)
        subprocess.Popen(["python3", "/home/pi/PlasticMonkeysCanSat/code/sensors/loraLogTail2W.py"])
    sleep(0.1)
