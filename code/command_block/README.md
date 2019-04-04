# Command Block

#### Requirements:
  Path to input file `rx.in` with packets converted to strings  
  Path to file with cameras timestamps: `camera.txt` (when the photos were taken)  
  Path to file with thermal camera timestamps: `thermal.txt` 
  Path to oled driver script: `oled.py`
  Path to lora status file: `lora_status.txt`
  
#### How it works:
  Each 0.1s command_block reads the recent recieved packet from the rx.txt file and analyzes the first charachter (line[0]) in the
  packet. After that, it runs a adequate function.
  
#### Command headers:

  ##### I
  Request for a regular image from camera. Requires a destinated timestamp at `line[1]` - `line[5]` and quatlity at `line[6]`
  ##### T
  Request for a thermal image from camera. Requires a destinated timestamp at `line[1]` - `line[5]`
  ##### R
  Request for a reboot. Requires command_block running as a root
  ##### S
  Request for a system info. Sends back cpu usage, battery percentage, free disk space
  ##### P
  Appends text from a packet to Oled Screens buffer.
  ##### H
  Prints general system stats on an Oled screen.
  
  

  
  
