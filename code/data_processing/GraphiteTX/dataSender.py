import graphyte
import random
import time

graphyte.init('localhost', prefix='cansat.random')

while True:
    data = random.randint(30,50)
    graphyte.send('foo.bar', data)
    print('sending: ' + str(data))
    #time.sleep(0.5);
