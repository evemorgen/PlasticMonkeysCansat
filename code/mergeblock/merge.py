#Jakub Podolak for Plastic Monkeys Cansat 2019

import configparser
import msgpack
import time
import sys
import re
import logging

#function to read paths to sensors' logs from config file
def get_directories(config):
    paths = config.items("PATHS")
    directories = [second for first,second in paths]
    return directories

#function reads sensors' names from config file
def get_keys(config):
    keys = []
    paths = config.items("PATHS")
    for key, path in paths:
        keys.append(key)
    return keys

#function takes paths to logs as an argument, returns list of the latest readings(int) from all paths
def get_tails(directories,length):
    tails = []
    for x in directories:
        with open(x, 'rb') as fh:
            fh.seek(-1*length, 2)
            last = fh.readlines()[-1].rstrip().decode()
        all_numbers = re.findall('\d+',last)
        number = int(all_numbers[-1])
        tails.append(number)
    return tails

#function takes tails and makes a dict
def prepare_dict(tails,keys):
    dict_pack = dict(zip(keys,tails))
    return dict_pack

#function takes list of latest readings (ints) and returns ready-to-send serialized packet
def prepare_message_pack(string_packet):
    return msgpack.packb(string_packet,use_bin_type="True")

#function prints new line to binary-typed file (to disjoin binary packets)
def binary_new_line(out):
    line = "\n"
    out.write(line.encode('utf-8'))

#prepares packet: ONE_BYTE_SIZE + MSGPACKED_DICT + FILL
def prepare_packet(message_pack, packet_length):
    return bytes([len(message_pack)]) + message_pack + bytes(b'-'*(packet_length-1-len(message_pack)))

def run():
    #initialize config parser, read from config file passed as an argument
    config_file = sys.argv[1]
    config = configparser.ConfigParser()
    config.read(config_file)

    #open log file
    logging.basicConfig(filename="mergeblock.log",level=logging.INFO)
    logging.info("Program starts to run...")

    #read some settings from config file
    output_path = config['SETTINGS']['output']
    datalog_path = config['SETTINGS']['datalog']
    sleep_time = float(config['SETTINGS']['sleeptime'])
    exception_sleep_time = float(config['SETTINGS']['exception_sleep_time'])
    line_length = int(config['SETTINGS']['line_length'])
    packet_length = int(config['SETTINGS']['packet_length'])
    prep_text_packs = config['SETTINGS'].getboolean('text_pack')
    directories = get_directories(config)
    keys = get_keys(config)

    while True:
        try:
            tails = get_tails(directories,line_length)
            dict_pack = prepare_dict(tails,keys)

            if prep_text_packs:
                datalog = open(datalog_path,"a")
                datalog.write(str(dict_pack) + '\n')
                datalog.close()

            msg_packet = prepare_message_pack(dict_pack)
            packet = prepare_packet(msg_packet, packet_length)
            output = open(output_path,"ab")
            output.write(packet)
            #binary_new_line(output)
            output.close()
            time.sleep(sleep_time)

        except Exception:
            logging.exception("Unexpected Exception!")
            time.sleep(exception_sleep_time)

run()
