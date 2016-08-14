#!/usr/bin/python

import dbus
import os
import subprocess
from dbus.mainloop.glib import DBusGMainLoop
import gobject

import subprocess

# ID of the device we care about
DEV_ID = 'CC:C3:EA:A5:1A:95'.replace(":", "_")

dbus_loop = DBusGMainLoop()
bus = dbus.SystemBus(mainloop=dbus_loop)

# Figure out the path to the headset
man = bus.get_object('org.bluez', '/')
iface = dbus.Interface(man, 'org.bluez.Manager')
adapterPath = iface.DefaultAdapter()

print(adapterPath + '/dev_' + DEV_ID)
headset = bus.get_object('org.bluez', adapterPath + '/dev_' + DEV_ID)
# ^^^ I'm not sure if that's kosher. But it works.

def cb(*args, **kwargs):
    is_connected = args[-1]
    if isinstance(is_connected, dbus.Boolean) and is_connected:
        print("Connected")
    elif isinstance(is_connected, dbus.Boolean) and not is_connected:
        print("Disconnected")
        subprocess.call(['/usr/bin/gnome-screensaver-command', '-l'])

headset.connect_to_signal("PropertyChanged", cb, interface_keyword='iface', member_keyword='mbr', path_keyword='path')

loop = gobject.MainLoop()
loop.run()

