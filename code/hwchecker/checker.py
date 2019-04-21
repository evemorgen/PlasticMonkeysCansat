#!/usr/bin/python3

import subprocess
import logging
import sys
try:
    import coloredlogs
except Exception:
    print("please install coloredlogs first: pip3 install coloredlogs")

coloredlogs.install()


def check(name, commands=None, install=None, function=None):
    logging.info("Checking {}".format(name))
    if function is not None:
        return function()
    result = subprocess.Popen([commands], shell=True, stdout=subprocess.PIPE)
    code = result.wait()
    if code != 0:
        logging.error("ERR")
        return install
    logging.info("OK")
    return {}


def test_lora():
    try:
        from SX127x.LoRa import LoRa
        from SX127x.board_config import BOARD
    except Exception as e:
        return {"pip": ["pyLora"]}
    try:
        BOARD.setup()
        lora = LoRa()
        lora.set_freq(434.2)
        freq = lora.get_freq()
        if int(freq) == 0:
            raise Exception("Not connected")
        assert 434.15 < freq < 434.25
        return {}
    except AssertionError:
        return {"hardware": ["bad frequency on LoRa radio"]}
    except Exception:
        return {"hardware": ["probably no connection to LoRa radio over SPI"]}


checks = [
    check("i2c tools", "i2cdetect -y 1", {"apt": ["python-smbus", "i2c-tools"], "script": ["raspi-config nonint do_i2c 0"]}),
    check("gryo, accel", "i2cdetect -y 1 | grep 6a", {"hardware": ["BerryGPS-IMU malfunction gyroscope"]}),
    check("compass", "i2cdetect -y 1 | grep 1c", {"hardware": ["BerryGPS-IMU malfunction compass"]}),
    check("bme280", "i2cdetect -y 1 | grep 77", {"hardware": ["BerryGPS-IMU malfunction bme280"]}),
    check("gps serial", "timeout -k 5 --preserve-status 5 head -n1 /dev/serial0", {"hardware": ["BerryGPS-IMU malfunction gps "]}),
    check("gpsd", "gpsd -V", {"apt": ["gpsd-clients gpsd screen"], }),
    check("bme680", "i2cdetect -y 1 | grep 76", {"hardware": ["OLED malfunction bme680"]}),
    check("oled display", "i2cdetect -y 1 | grep 3c", {"hardware": ["OLED malfunction display"]}),
    check("gpiozero", "ls /usr/local/lib/python3.5/dist-packages | grep gpiozero", {"pip": ["gpiozero"], "apt": ["python-dev", "python-rpi.gpio"]}),
    check("pylora", "ls /usr/local/lib/python3.5/dist-packages | grep -i pyLoRa", {"pip": ["pyLoRa", "spidev", "RPi.GPIO"], "apt": ["python-dev", "python-rpi.gpio"], "script": ["raspi-config nonint do_spi 0"]}),
    check("lora communication", function=test_lora),
    check("thermal camera", "i2cdetect -y 1 | grep 33", {"hardware": ["MODULE malfunction thermal camera"]}),
    check("thermal camera software", "dpkg -l | grep -i libi2c-dev", {"apt": ["libi2c-dev", "git", "libjpeg-dev", "zlib1g-dev"], "script": ["echo 'dtparam=i2c1_baudrate=400000' >> /boot/config.txt", "git clone https://github.com/pimoroni/mlx90640-library.git; cd mlx90640-library; make clean; make I2C_MODE=LINUX"], "pip": ["pillow"]}),
    check("normal camera enabled", "raspi-config nonint get_camera | grep 0", {"script": ["raspi-config nonint do_camera 0"]}),
    check("normal camera connected", "raspistill -o /dev/null", {"hardware": ["normal camera not connected"]})
]


things = {
    "apt": [],
    "pip": [],
    "script": [],
    "hardware": []
}

for todo in checks:
    for thing in things:
        if thing in todo:
            things[thing].extend(todo[thing])

if "--hardware" not in sys.argv:
    if things["apt"] != []:
        logging.warning("missing system packages, install them with:\n    sudo apt install %s", " ".join(things["apt"]))
    if things["pip"] != []:
        logging.warning("missing python packages, install them with:\n    pip3 install %s", " ".join(things["pip"]))
    if things["script"] != []:
        logging.warning("missing system configuration, set them up running the following scripts:\n    %s", "\n    ".join(things["script"]))
logging.error("disconnected hardware detected:\n    %s", "\n    ".join(things["hardware"]))
