#Jakub Podolak for Plastic Monkeys Cansat 2019

import subprocess
import configparser
import msgpack
import time

#our command to get one last line from file
tail_command = "tail -n 1 "

#initialize config parser, read from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

#read some settings from config file
output_path = config['SETTINGS']['output']
datalog_path = config['SETTINGS']['datalog']
sleep_time = float(config['SETTINGS']['sleeptime'])

#function to read paths to sensors' logs from config file
def getDirectories():
    directories = []
    paths = config.items("PATHS")
    for key, path in paths:
        directories.append(path)
    return directories

#function takes paths to logs as an argument, returns list of the latest readings(int) from all paths
def getTails(directories):
    tails = []
    for x in directories:
        command = tail_command + x
        result = subprocess.Popen(command.split(), stdout=subprocess.PIPE).communicate()[0]
        result.rstrip()
        s = str(result, 'utf-8')
        number = int(s)
        tails.append(number)
    return tails

#function takes list of latest readings (ints) and returns packet in readable form
def prepareTextPack(tails):
    text_pack = ''
    for x in tails:
        text_pack = text_pack + str(x) + ';'
    text_pack = text_pack + '\n'
    return text_pack

#function takes list of latest readings (ints) and returns ready-to-send serialized packet
def prepareMessagePack(tails):
    message = msgpack.packb(tails,use_bin_type="True")
    return message

#function prints new line to binary-typed file (to disjoin binary packets)
def binaryNewLine(out):
    line = str(0) + "\n"
    out.write(line.encode('utf-8'))

directories = getDirectories()

while True:
    output = open(output_path,"ab")
    datalog = open(datalog_path,"a")

    tails = getTails(directories)
    msg_packet = prepareMessagePack(tails)
    text_packet = prepareTextPack(tails)

    output.write(msg_packet)
    binaryNewLine(output)

    datalog.write(text_packet)
    datalog.close()
    output.close()
    time.sleep(sleep_time)
