# Data Processor Block
#### Takes packets with data from base_parser and sends it to graphyte
### Run it:
`python data_processor.py config.ini`
### Config File:
`config.ini` - You specify here your graphite address (if you host it on the same device its `localhost`), graphyte prefix (kinda like folder with your data in graphyte) and sleep_time  
Also you provide paths to logs with packets here. Sample `config.ini` file:
```
[SETTINGS]
graphyte_address = localhost
graphyte_prefix = cansat
sleep_time = 0.2

[PATHS]
primary = primary_log.txt
secondary = secondary_log.txt
```
  
### Input packets format:
Each packet should consist of 40 chars:  
(2 chars of dict length) - (dict) - (fill to 40 chars)  
example:  
`16{'s': 6, 'g': 2}----------------------`

### Logging
Automatically logs the received dict to `data_processor.log`. 
