# How to get it working? (Debian)

### Step 1 - Install docker

Jump here and follow those steps: [Get Docker](https://docs.docker.com/install/linux/docker-ce/debian/) 

You can also find installation guides for all systems here

### Step 2 - Install graphite 

Just type in your terminal:

>docker run -d\
 --name graphite\
 --restart=always\
 -p 80:80\
 -p 2003-2004:2003-2004\
 -p 2023-2024:2023-2024\
 -p 8125:8125/udp\
 -p 8126:8126\
 hopsoft/graphite-statsd

### Step 3 - Install Python graphite library:

To complete this step you need to have both Python and pip installed. You can google it very easily.
Then you can install our library:

>pip install graphyte

### Step 4 - Open Graphite dashboard

Jump to your favourite web browser and type in URL bar:

>localhost

You should get access to our graphite dashboard. If your graphite is not alive you can start it:

>docker start graphite

### Step 5 - Start sending some data

Now you can run script provided in this repo, it should send some random numbers between 30 and 40 to your graphite base. You can find them
in a directory:

> Metrics/cansat/random/foo/bar

So you can choose this file in your graphite dashboard and see a nice graph of flowing data.

### Step 6 - Increase retention (frequency of accepting data)

By default our Graphite base can obtain one number for 10s. You can make it faster or slower by changing some files.
Execute when graphite is running:

> docker exec -it graphite bash

End edit a file:

> /opt/graphite/conf/storage-schemas.conf

Change two lines with retentions settings like that:

> retentions = 10s/...

to 

> retentions = 1s/...

Now save it and go to the directory 

> /opt/graphite/storage

and erase all data which we've obtained before. You can do it just by erasing the whole folder "whisper"

> rm -r whisper

This folder should be created automatically again when we send something to the graphite base. If it's not, simply create it again:

> mkdir whisper

This should increase retention.






