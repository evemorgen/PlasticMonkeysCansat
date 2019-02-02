# The most epic guide to daemons using supervisord

### 1. Install your supervisord
```
pip install supervisor
```
or download it with instructions on [supervisord website](http://supervisord.org/installing.html)

### 2. Find where your supervisord is

In my case it was `/usr/local/bin`, You should also find your supervisord.conf and supervisord.log here

### 3. Change your supervisord.conf file

This way you can add your own script, you can test if everything works using this conf:

```
[supervisord]
[program:foo]
command = /bin/cat
```
To edit this file you will need to edit it as a root user, there are many ways to do that. I prefer
`sudo nano supervisord.conf` or entering `su` in terminal, and then `gedit supervisord.conf`.

### 4. Start your supervisord program
Type `sudo supervisord` - 
It will run cat editor in the background. You can check it using `supervisord.log` file. You should see, that your
program `foo` is spawned with unique PID. 

### 5. Try to kill this process
yeee fun part. When you know your process PID type:
`sudo kill <PID>` replacing <PID> with your process PID. Ha! Now it's dead! Well... actually not. Check your log file.
This madman is unstoppable. It just has respawned. Or should.

### 6. Turn the whole thing off
`sudo pkill supervisord`

### 7. Wipe your log file
`sudo cat /dev/null > supervisord.log`

### 8. What next?
You can use it to keep your python script living. I have provided here a sample log file running dataSender.py python
script. Check it out!
