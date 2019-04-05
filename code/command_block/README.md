# Command Block

#### Requirements:
  Needs:  
  Path to input file `rx.in` with packets converted to strings  
  Path to file with cameras timestamps: `camera.txt` (when the photos were taken)  
  Path to file with thermal camera timestamps: `thermal.txt`  
  Path to lora status file: `lora_status.txt`  
  Path to oled buffer file: `buffer.txt`  
  
  ##### Note:
  It supports only 11 characters packets - 1 Header character + 10 data characters
  
  
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
  ##### A
  Appends text from a packet at `line[1] - line[10]` to oled Screens buffer.
  ##### C  
  Clears oled buffer  
  
  

  
  
