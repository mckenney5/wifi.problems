#!/bin/python3.8
import os
import time


# Main File, back-end

def wifi_addapter(state):
    if state == True:
        print("Enabling Adapter")
        # Enable adapter (os.system)
    else:
        print("Disabling Adapter")
        # Disable Adapter (os.system)


def power_cycle():
    # os.system("sudo reboot")
    os.system("echo test")


def is_offline():
    # TODO check if user is online via ping
    hostname = "8.8.8.8"  # Google DNS
    response = os.system("ping -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        return False
    else:
        return True


log = [time.asctime(time.localtime(time.time())) + "Start"]

# control loop
while True:
    if is_offline():
        if is_offline() & is_offline():
            # if the user is offline, triple check
            log.append(time.asctime(time.localtime(time.time())) + "Offline")
    else:
        print("OK")
    time.sleep(10)
    # log
    # notify the user
    # try to disable and enable the adapter
    # check if online
    # if not, recommend a power cycle
    #   powercycle
    #   check again (sleep), if still not working, recommend a hard reset
    # log when back online with a duration
