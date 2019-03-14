from picamera import PiCamera
from time import sleep, time
import sys
from PIL import Image


camera = PiCamera()
camera.start_preview()
sleep(1)

t = str(round(time()) % 86400)
camera.capture('/home/pi/images/'+ t + '-raw.jpg')
camera.stop_preview()

qual = {
    'low': (160, 120),
    'medium': (320, 240),
    'high': (640, 480)
}

raw = Image.open('/home/pi/images/'+ t + '-raw.jpg')

for key in qual:
    img = raw.resize(qual[key], Image.ANTIALIAS)
    img.save('/home/pi/images/'+ t + '-' + key + '.jpg')

