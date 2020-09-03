# install some sdeps
# pip install mido
# pip install python-rtmidi

#

import mido
import random
from mido.sockets import PortServer, connect

# for message in connect('localhost', 8988):
#     print(message)


output = connect('localhost', 8988)
while True:
    message = mido.Message('note_on', note=random.randint(0,127), velocity=3, time=6.2)
    output.send(message)