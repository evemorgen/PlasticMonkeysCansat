# Raspbian Headless installation:

1 [Download latest raspbianhttps](://www.raspberrypi.org/downloads/)
2 Flash it on SD Card using [Etcher](https://www.balena.io/etcher/ (Windows))
3 Eject the card and plug it in again
4 Create new file in boot directory: `wpa_supplicant.conf`  
- Write to this file:
```bash
country=PL
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
	ssid="MyWiFiNetwork"
	psk="aVeryStrongPassword"
	key_mgmt=WPA-PSK
}
```
- Create an empty file called `ssh` (without any extension)
- Insert card to raspberry, wait for it to connect
- Switch to Linux
- Using Linux program nmap or in your router details find raspberrys IP address
- Connect to SSH using this command:  `ssh pi@<IP>`
(replace <IP> with raspberryPi adress, e.g. `ssh pi@192.168.1.1`)
- Login using password: raspberry
That's it!

You can exit using the command: `exit` 
And format your sd card using program DISKPART from your cmd (Windows), in cmd:
```bash
diskpart  
list disk  
select disk x  
clean  
create partition primary  
```
Links:
<https://core-electronics.com.au/tutorials/raspberry-pi-zerow-headless-wifi-setup.html>
<https://www.raspberrypi.org/documentation/remote-access/ssh/unix.md>


# Running script at boot:
```
sudo nano /etc/rc.local    
```
And add your command before *exit 0*, for instace:  
```
sudo python /home/pi/blink.py 
```

# To create a backup of SD Card:
```
sudo fdisk -l </br> 
```

will list all disks with their names and localizations  
```
sudo dd if=/dev/mmcblk0 of=~/beacan1.img
```
will copy everything to our new backup image.

from `dd` man page:
> if=file  Read input from file instead of the standard input.
> of=file  Write output to file instead of the standard output.  Any regular output file is truncated unless the notrunc conversion value is specified.  If an initial portion of the output file is seeked past (see the oseek operand), the output file is truncated at that point.
