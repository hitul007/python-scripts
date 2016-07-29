"""
We are hearing music in at some place and suddenly we exclude headphones and speaker turn on.
This script will mute audio whenever headphone unplugged.
"""

#!/usr/bin/python
import socket
import sys
import subprocess
import datetime
import time

"""
amixer -D pulse sset Master 100%+
"""

server_address = '/var/run/acpid.socket'
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

try:
    sock.connect(server_address)
except socket.error, msg:
    print msg
    sys.exit(1)

days = ['monday', 'tuesday', 'wednessday', 'thursday', 'friday']

while True:
    msg = sock.recv(4096)
    if msg:
        if not datetime.datetime.now().strftime('%A').lower() in days:
            time.sleep(5)
            continue

        msg = msg.split('\n')
        if(len(msg) > 1):
            msg = msg[0]
            event_name = msg

        if 'HEADPHONE plug' in event_name:
            print("plugged")

        elif 'HEADPHONE unplug' in event_name:
            subprocess.call(["amixer", "-D", "pulse", "sset", "Master", "100%-"])
            print("UnPlugged")

