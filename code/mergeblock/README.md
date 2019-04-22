# Easy Merge Block

### How to use:
in config.ini specify your settings:  
`output` = path to file where binary ready-to-send packets are going to be stored, will be created if it doesn't exist  
`datalog` = path to file where readable packets are going to be stored, will be created if it doesn't exist  
`sleeptime` = delay before merges  
`line_length` = your maximum line length in sensors' logs - how many bytes script have to load to RAM to load last line  
`text_packets` = yes or no - set to yes if you want to have readable packets  
`exception_sleep_time` = delay after getting an exception  
`packet_length` = number of bytes in output packet  

You also specify paths to all logs that we want to merge in `[PATHS]` section like this:
```
[PATHS]
path1 = foo1.log
path2 = /home/xyz/Desktop/foo2.log
path3 = /home/sensors/temperature/temp.log
```

### Output:
Packet of `packet_length` size in `bytes`:  
one byte describing data_dict size + msgpacked data_dict + fill ('-') to `packet_length`  

### Start:
Next you can run your mergeblock using: `python3 merge.py`  
Libraries used: configparser, msgpack, time, sys, re, logging
