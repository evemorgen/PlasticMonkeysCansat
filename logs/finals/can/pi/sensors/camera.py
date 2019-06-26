from picamera import PiCamera
from time import sleep, time
import sys
from PIL import Image

#f = open("/home/pi/sensor_logs/camera.txt", "w")
#f.close()

qual = {
    'low': (160, 120),
    'medium': (320, 240),
    'high': (640, 480),
    'ultra': (1600, 1200)
}

camera = PiCamera()
camera.start_preview()
sleep(1)

while True:
    t = str(round(time()) % 86400)
    log = open("/home/pi/sensor_logs/camera.txt", "a")
    log.write(t + "\n")

    camera.capture('/home/pi/images/'+ t + '_raw.jpg')
    camera.stop_preview()

    raw = Image.open('/home/pi/images/'+ t + '_raw.jpg')

    for key in qual:
        img = raw.resize(qual[key], Image.ANTIALIAS)
        img.save('/home/pi/images/'+ t + '_' + key + '.jpg')
    sleep(10)

