# Command Block

#### Requirements:
  Needs config.ini with specified:  
  `camera_log_file` - file where photos' timestamps appear  
  `thermal_log_file` - file where thermal photos' timestamps appear  
  `oled_text_buffer` - file from which the text will be read on OLED, and where we will append text  
  `lora_status_file` - file where lora commands will appear  
  `rx_file` - file with recieved string-packets to process  
  `sleep_time` - delay time in seconds (float) between processing new messages  
  `exception_sleep_time` - delay time in seconds (float) after getting a exception  
  `packet_line_length` - length of a packet, at least 7  
  `time_stamp_length` - number of characters used in packet to describe a timestamp  
  
  
  
  ##### Note:
  First character in each packet should be a one char header!
  
  
#### How it works:
  Each sleep_time command_block reads the recent recieved packet from the rx_file if new line popped in. After that it analyzes the first charachter (line[0]) in the packet. Afterwards, it runs a adequate function.
  
#### Command headers:

  ##### I
  Request for a regular image from camera. Requires a destinated timestamp at `line[1]` - `line[timestamp_length]` and quatlity at `line[timestamp_length+1]`
  ##### T
  Request for a thermal image from camera. Requires a destinated timestamp at `line[1]` - `line[timestamp_length]`  
  ##### R
  Checks `line[0]` - `line[5]` for `'REBOOT'` command. Request for a reboot. Requires command_block running as a root
  ##### S
  Request for a system info. Sends back cpu usage, battery percentage, free disk space
  ##### A
  Appends text from a packet from `line[1]` to `line[packet_line_length-1]` to oled Screens buffer.
  ##### C  
  Clears oled buffer  
