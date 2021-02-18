#!/bin/python3.8
import os
import sys
import time

# Default Variables
enable = True
disable = False
offline_flag = False
running_log = ['[' + time.asctime() + "] Start"]
debug_log = ['[' + time.asctime() + "] Start"]


# Main File, back-end

def debug(msg):
    # Adds to the debugging log so the user can see what the program is doing
    debug_log.append('[' + time.asctime().split(" ")[3] + '] ' + msg)

    # uncomment if you want debugging info logged in the console
    diagnostic = sys.stderr.write
    diagnostic('[' + time.asctime().split(" ")[3] + '] ' + msg)

def log(msg):
    # Adds to the running log and appends the hard copy of the log
    running_log.append('[' + time.asctime().split(" ")[3] + '] ' + msg)
    # log_file = open("/var/log/wifi.problems.log", "a")
    log_file = open("/tmp/wifi.problems.log", "a")
    log_file.write(time.asctime(time.localtime(time.time())) + msg)
    log_file.close()


def wifi_adapter(state):
    if state == enable:
        debug("Enabling Adapter")
        # Enable adapter (os.system)
    else:
        debug("Disabling Adapter")
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
    output = os.system('xmessage -center ' + msg + ' -buttons Yes:2,No:0,"View Logs":3,"View Debugging '
                                                   'Information":4,Cancel:0') >> 8
    if output == 2:
        return True  # os.system returns a binary number, shifting the bits 8 to the right
        # converts it to a 2 for yes or 0 for no
    elif output == 3:
        # display the current log for this session
        full_log = "Today:"
        for item in running_log:
            full_log = full_log + "\n" + item
        os.system('xmessage -center "' + full_log + '"')
        return prompt_user(msg)
    elif output == 4:
        # display the current debugging log for this session
        full_log = "Diagnostic Information:"
        for item in debug_log:
            full_log = full_log + "\n" + item
        os.system('xmessage -center "' + full_log + '"')
        return prompt_user(msg)
    else:
        return False


def attempt_fix():
    # first try to get online again
    debug("Attempting to toggle wireless adapter")
    wifi_adapter(disable)
    time.sleep(5)
    wifi_adapter(enable)
    time.sleep(5)
    if is_offline():
        debug("Still offline")
        if prompt_user("Toggle failed. Would you like to restart your computer? NOTE: If this does not work, "
                       "you need to hard reset your computer by holding the power button down."):
            power_cycle()


# control loop
while True:
    if is_offline():
        if is_offline() & is_offline():
            # if the user is offline, triple check
            if offline_flag == False:
                log("Offline")
                offline_flag = True

            if prompt_user("You are offline! Would you like me to try to fix this?"):
                attempt_fix()
            debug("Sleeping for 5 minutes...")
            time.sleep(5 * 60)  # if the user said no, sleep for five minutes
    else:
        debug("Online. Checking again in 10 seconds...")
        if offline_flag == True:
            log("Back Online")
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
