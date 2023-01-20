# Data Processor Block
#### Takes packets with data from base_parser and sends it to graphyte
### Run it:
`python3 data_processor.py config.ini`
### Config File:
`config.ini` - You specify here your graphite address (if you host it on the same device its `localhost`), graphite prefix (kinda like folder with your data in graphite), sleep_time, sleep_time after exception, and length of received packets 
Also you provide paths to logs with packets here. Sample `config.ini` file:
```
[SETTINGS]
graphyte_address = localhost
graphyte_prefix = cansat
sleep_time = 0.2
exception_sleep_time = 0.5
packet_length = 30

[PATHS]
default = out.log
```
  
### Input packets format:
Each packet should consist of fixed number of bytes(chars):  
(1 char (byte) of dict length) - (msgpacked dict) - (filler)
example:  
`b'\x07\x82\xa1a\x14\xa1b\x0c----------------------\n'`

### Logging
Automatically logs the received dict and exceptions to `data_processor.log`. 
