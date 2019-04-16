# OLED_BLOCK

### Get this bad boy working:  
Just follow [this](https://www.raspberrypi-spy.co.uk/2018/04/i2c-oled-display-module-with-raspberry-pi/) tutorial.

### How it works?
Program should have access to oled_buffer.txt file, you can specify the path in the code.  
It reads a file and converts it into string, ignoring new lines (`'\n'`) and "fillers" (`'-'`).  
After that it splits a message into lines, you can define width of them in code, and prints them.  
It also adds hyphens where it's necessary.  
It repeats the process, with delay equal to `sleep_time` variable specified in code.
