#Jakub Podolak for Plastic Monkeys Cansat 2019

import graphyte
from time import sleep
import ast
import configparser
import sys

config_file = sys.argv[1]
config = configparser.ConfigParser()
config.read(config_file)
graphyte_address = config['SETTINGS']['graphyte_address']
graphyte.init(graphyte_address, prefix='cansat')

#function to read paths to input logs from config file
def get_directories(config):
    paths = config.items("PATHS")
    directories = [second for first,second in paths]
    return directories

#extracts dict from string packet
def trim_line(line):
    dict_len = int(line[0:2])
    return line[2:2+dict_len]

#converts string-dict to dict
def get_dict(line):
    return ast.literal_eval(line)

def send_to_graphite(data_dict):
    for name,val in data_dict.items():
        graphyte.send(name,val)

def run():
    directories = get_directories(config)

    while True:
        try:
            for input_log in directories:
                file = open(input_log, "r")
                file.seek(0,2)
                file.seek(file.tell()-41, 0) #Packet should have a size of 40 characters
                line = file.readline()
                line = trim_line(line)
                data_dict = get_dict(line)
                send_to_graphite(data_dict)
                sleep(0.1)
        except Exception:
            sleep(0.1)

run()
