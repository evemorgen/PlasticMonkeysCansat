#Jakub Podolak for Plastic Monkeys Cansat 2019

import graphyte
from time import sleep
import ast
import configparser
import logging
import msgpack
import sys

config_file = sys.argv[1]
config = configparser.ConfigParser()
config.read(config_file)

graphyte_address = config['SETTINGS']['graphyte_address']
graphyte_prefix = config['SETTINGS']['graphyte_prefix']
sleep_time = float(config['SETTINGS']['sleep_time'])
exception_sleep_time = float(config['SETTINGS']['exception_sleep_time'])
packet_length = int(config['SETTINGS']['packet_length'])

graphyte.init(graphyte_address, prefix=graphyte_prefix)

#open log file
logging.basicConfig(filename="data_processor.log",level=logging.INFO)

#function to read paths to input logs from config file
def get_directories(config):
    paths = config.items("PATHS")
    directories = [second for first,second in paths]
    return directories

#extracts dict from line
def trim_line(line):
    dict_len = int(line[0])
    return line[1:1+dict_len]

#converts msgpacked bytes to dict
def get_dict(line):
    return msgpack.unpackb(line,raw=False)

def send_to_graphite(data_dict):
    for name,val in data_dict.items():
        graphyte.send(name,val)

def run():
    directories = get_directories(config)

    while True:
        try:
            for input_log in directories:
                file = open(input_log, "rb")
                file.seek(0,2)
                file.seek(file.tell()-(packet_length+1), 0)
                line = file.readline()
                line = trim_line(line)
                data_dict = get_dict(line)
                logging.info(data_dict)
                send_to_graphite(data_dict)
                sleep(sleep_time)
        except Exception:
            logging.exception("Unexpected Exception!")
            sleep(exception_sleep_time)

run()
