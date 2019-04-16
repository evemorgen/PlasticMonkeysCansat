# Data Processor Block
#### Takes packets with data from base_parser and sends it to graphyte
### Run it:
`python data_processor.py config.ini`
### Config File:
`config.ini` - You specify here your graphite address, if you host it on the same device its `localhost`.  
Also you provide paths to logs with packets here. Sample `config.ini` file:
```
[SETTINGS]
graphyte_address = localhost

[PATHS]
primary = primary_log.txt
secondary = secondary_log.txt
```
  
### Input packets format:
Each packet should consist of 40 chars:  
(2 chars of dict length) - (dict) - (fill to 40 chars)  
example:  
`16{'s': 6, 'g': 2}----------------------`
