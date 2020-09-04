#!/usr/bin/python3

import os
import time

BINPATH = "../bin/"
PORT = "USB1"
PROGRAMMER = "~/local/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI"
# PROGRAMMER = "~/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI"

def doPull():
    os.system("git pull")

def update(board):
    com = PROGRAMMER + " -c port=" + PORT + " -w " + BINPATH + board + ".bin 0x8000000 --start"
    #  print(com)
    ret = os.system(com)
    # should be zero if successful
    if ret:
        print("Failed")
        return ret
    timeout = 5 # 5 seoncds
    interval = 0.1 # .1 seconds
    # loop until device comes up or timesout
    while timeout:
        if os.path.exists("/dev/" + board):
            print("Success")
            return 0
        timeout = timeout - interval
        time.sleep(interval)
    print("Failed")
    return 1

# If called as submodule name will be name of this script
if __name__ == "__main__":
    update("cabinet")
