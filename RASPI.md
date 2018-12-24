# Raspbian Headless installation:

1. [Download latest raspbianhttps](://www.raspberrypi.org/downloads/)
2. Flash it on SD Card using [Etcher](https://www.balena.io/etcher/ (Windows))
3. Eject the card and plug it in again
4. Create new file in boot directory: `wpa_supplicant.conf`  
5. Write to this file:
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
6. Create an empty file called `ssh` (without any extension)
7. Insert card to raspberry, wait for it to connect
8. Switch to Linux
9. Using Linux program nmap or in your router details find raspberrys IP address
10. Connect to SSH using this command:  `ssh pi@<IP>`
(replace <IP> with raspberryPi adress, e.g. `ssh pi@192.168.1.1`)
11. Login using password: raspberry
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

# Raspbian lifting

1. Adding a new user:
`sudo adduser username`
or new user with administrative privileges: `sudo adduser username sudo`

2. Deleting user:
`sudo userdel username`
Then you may want to delete the home directory for the deleted user account :
`sudo rm -r /home/username`

3. To modify the username of a user (must be done from another account):
`sudo usermod -l new_username old_username`

4. Changing the password:
`sudo passwd username`

5. To list all users:
`compgen -u`

6. Adding fat32 partition
`sudo fdisk /dev/mmcblk0`
By writing `p` you can display more details about your disk.
Execute command `n` to create new partition.
Select `p` (primary partition).
Select partition number, first and last sector.
Your partition has been created, now you have to change its type:
Execute command `t` and choose the partition you want to change.
Set partition id as `b` (it stands for FAT32).
Write changes: `w` and reboot.
Now FAT32 file-system can be created from command line with mkfs:
`sudo mkfs -t vfat /dev/mmcblk0pn` (where n is the partition number you have chosen) 

7. Enable I2C
`sudo raspi-config`
Choose Interfacing options, then I2C and finally Yes.

8. Enable serial port
`sudo raspi-config`
Choose Interfacing options, then Serial, answer No to the question about login shell and Yes to the question about serial hardware port.

9. Enable serial gadget
Open up the `config.txt` file that is in the SD card.
Go to the bottom and add `dtoverlay=dwc2as` the last line.
Save the config.txt file as plain text and then open up `cmdline.txt` After rootwait (the last word on the first line) add a space and then `modules-load=dwc2,g_serial`
More: https://learn.adafruit.com/turning-your-raspberry-pi-zero-into-a-usb-gadget/serial-gadget

10. Enable ethernet gadget
Open up the `config.txt` file that is in the SD card.
Go to the bottom and add `dtoverlay=dwc2as` the last line.
Save the config.txt file as plain text and then open up `cmdline.txt` After rootwait (the last word on the first line) add a space and then `modules-load=dwc2,g_ether`
In case of any troubles: https://learn.adafruit.com/turning-your-raspberry-pi-zero-into-a-usb-gadget/ethernet-gadget

11. Disable bluetooth
Go to `sudo nano /boot/config.txt`
Add below, save and close the file.
```
# Disable Bluetooth
dtoverlay=pi3-disable-bt
```
Disable related services:
```
sudo systemctl disable hciuart.service
sudo systemctl disable bluealsa.service
sudo systemctl disable bluetooth.service
```

Disable Bluetooth completely
If Bluetooth is not required at all, uninstall Bluetooth stack. It makes Bluetooth unavailable even if external Bluetooth adapter is plugged in.
```
sudo apt-get purge bluez -y
sudo apt-get autoremove -y`
```

12. Disable HDMI
`sudo nano /etc/rc.local`
Add the following lines above exit 0:
```
# Disable HDMI
/usr/bin/tvservice -o
```
