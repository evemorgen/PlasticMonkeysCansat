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
13. Installing Python 3.5

a. Install the required build-tools (some might already be installed on your system).

 ```
        sudo apt-get update
        sudo apt-get install build-essential tk-dev
        sudo apt-get install libncurses5-dev libncursesw5-dev libreadline6-dev
        sudo apt-get install libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev
        sudo apt-get install libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev
 ```

   If one of the packages cannot be found, try a newer version number (e.g. ``libdb5.4-dev`` instead of ``libdb5.3-dev``).

b. Download and install Python 3.5. When downloading the source code, select the most recent release of Python 3.5, available
   on the `official site <https://www.python.org/downloads/source/>`_. Adjust the file names accordingly.

```
        wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
        tar zxvf Python-3.5.2.tgz
        cd Python-3.5.2
        ./configure --prefix=/usr/local/opt/python-3.5.2
        make
        sudo make install
```
	

c. Make the compiled binaries globally available.

 ```
        sudo ln -s /usr/local/opt/python-3.5.2/bin/pydoc3.5 /usr/bin/pydoc3.5
        sudo ln -s /usr/local/opt/python-3.5.2/bin/python3.5 /usr/bin/python3.5
        sudo ln -s /usr/local/opt/python-3.5.2/bin/python3.5m /usr/bin/python3.5m
        sudo ln -s /usr/local/opt/python-3.5.2/bin/pyvenv-3.5 /usr/bin/pyvenv-3.5
        sudo ln -s /usr/local/opt/python-3.5.2/bin/pip3.5 /usr/bin/pip3.5
 ```

   You should now have a fully working Python 3.5 installation on your Raspberry Pi!
d. How to change from default to alternative Python version:
```
alias python='/usr/bin/python3.5'
. ~/.bashrc
```
14. GPS setup – described [here](http://ozzmaker.com/berrygps-setup-guide-raspberry-pi/)

At the beginnig: 
```
git clone http://github.com/ozzmaker/BerryIMU.git
```
Then update software and OS
```
sudo apt-get update
sudo apt-get upgrade
sudo reboot
```
Open raspi-config and disable serial console.

To display GPS data:
```
sudo apt-get install screen
screen /dev/serial0 9600
```

Install, gpsd, gpsmon and cgps;
```
sudo apt-get install gpsd-clients gpsd -y
```

If you need to stop gpsd, you can use
```
sudo killall gpsd
```

Be default, gpsd is configured to stat at boot and run in the background. If you are fine with this, you will need to edit the config file so that gpsd uses the correct serial device.
```
sudo nano /etc/default/gpsd
```
Look for
`DEVICES=""`
and change it to
`DEVICES="/dev/serial0"`
If you want to manually run gpsd, you will need to disable it from starting at boot;
```
sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket
```

To force it to autostart again at boot;
```
sudo systemctl enable gpsd.socket
sudo systemctl start gpsd.socket
```

You can now use gpsmon or cgps to view GPS data.

We will be using gpspipe to capture the NMEA sentence from the BerryGPS and storing these into a file. The command to use is;
```
gpspipe -r -d -l -o /home/pi/`date +"%Y%m%d-%H-%M-%S"`.nmea
```
-r = Output raw NMEA sentences.
-d = Causes gpspipe to run as a daemon.
-l = Causes gpspipe to sleep for ten seconds before attempting to connect to gpsd.
-o = Output to file.
Now we need to force the above command to run at boot. This can be done by editing the rc.local file.
```
sudo nano /etc/rc.local
```
Just before the last line, which will be 'exit 0', paste in the below line;
`gpspipe -r -d -l -o /home/pi/`date +"%Y%m%d-%H-%M-%S"`.nmea`

15. What do we need for IMU:

```
git clone http://github.com/ozzmaker/BerryIMU.git
sudo apt-get update
sudo apt-get install i2c-tools libi2c-dev python-smbus
sudo nano /etc/modprobe.d/raspi-blacklist.conf
```
Place a hash '#' in front of blacklist i2c-bcm2708
If the above file is blank or doesn't exist, then skip the above step
You now need to edit the modules conf file.
```
 sudo nano /etc/modules
```
Add these two lines;
```
i2c-dev
i2c-bcm2708
```
Update /boot/config.txt
```
sudo nano /boot/config.txt
```
Add to the bottom;
```
dtparam=i2c_arm=on
dtparam=i2c1=on
```
More: http://ozzmaker.com/berryimu/
