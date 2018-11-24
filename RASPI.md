**Raspbian Headless installation:**

- Download latest raspbian: https://www.raspberrypi.org/downloads/
- Flash it on SD Card using Etcher: https://www.balena.io/etcher/ (Windows)
- Eject the card and plug it in again
- Create new file in boot directory: wpa_supplicant.conf
- Write to this file:
country=PL
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
	ssid="MyWiFiNetwork"
	psk="aVeryStrongPassword"
	key_mgmt=WPA-PSK
}
- Create an empty file called ssh (without extension)
- Insert card to raspberry, wait for it to connect
- Switch to Linux
- Using Linux program nmap or in your router details find raspberrys IP address
- Connect to SSH using this command:  ssh pi@<IP>
(replace <IP> with raspberryPi adress, e.g. ssh pi@192.168.1.1)
- Login using password: raspberry
That's it!

You can exit using the command: exit  
And format your sd card using program DISKPART from your cmd (Windows), in cmd:
> diskpart  
> list disk  
> select disk x  
> clean  
> create partition primary  

Links:
https://core-electronics.com.au/tutorials/raspberry-pi-zerow-headless-wifi-setup.html
https://www.raspberrypi.org/documentation/remote-access/ssh/unix.md


**Running script at boot:**

> sudo nano /etc/rc.local    

And add your command before "exit 0", for instace:  

> sudo python /home/pi/blink.py 


**To create a backup of SD Card:**

> sudo fdisk -l </br> 

will list all disks with their names and localizations </br>

> sudo dd if=/dev/mmcblk0 of=~/beacan1.img </br> 

will copy everything to our new backup image.

if= is a directory of SD Card (from previous command) and of= is a output directory
