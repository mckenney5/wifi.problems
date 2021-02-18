#!/bin/python3.8
import os
import sys
import time

# Default Variables
enable = True
disable = False
offline_flag = False
log = [time.asctime(time.localtime(time.time())) + "Start"]
debug = sys.stderr.write


# Main File, back-end

def wifi_adapter(state):
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
    return True
    # checks if user is online via ping
    response = os.system("ping -c 1 8.8.8.8")  # ping Google's DNS once
    if response == 0:
        return False
    else:
        return True


def prompt_user(msg):
    if (os.system('xmessage -center ' + msg + ' -buttons Yes:2,No:0,'
                  'Cancel:0') >> 8) == 2:
        return True  # os.system returns a binary number, shifting the bits 8 to the right
                     # converts it to a 2 for yes or 0 for no
    else:
        return False


def attempt_fix():
    # first try to get online again
    debug("Attempting to toggle wireless adapter")
    wifi_adapter(disable)
    time.sleep(1)
    wifi_adapter(enable)
    time.sleep(5)
    if is_offline():
        debug("Still offline")
        if prompt_user("Toggle failed. Would you like to restart your computer?"):
            power_cycle()


# control loop
while True:
    if is_offline():
        if is_offline() & is_offline():
            # if the user is offline, triple check
            if offline_flag == False:
                log.append(time.asctime(time.localtime(time.time())) + "Offline")
                offline_flag = True

            if prompt_user("You are offline! Would you like me to try to fix this?"):
                attempt_fix()
            else:
                debug("User said no. Sleeping...")
            time.sleep(5 * 60)  # if the user said no, sleep for five minutes
    else:
        debug("OK")
        if offline_flag == True:
            log.append(time.asctime(time.localtime(time.time())) + "Back Online")
            offline_flag = False
    time.sleep(10)
    # log
    # notify the user
    # try to disable and enable the adapter
    # check if online
    # if not, recommend a power cycle
    #   powercycle
    #   check again (sleep), if still not working, recommend a hard reset
    # log when back online with a duration
