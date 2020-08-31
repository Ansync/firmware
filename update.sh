#!/bin/bash

BOARD=$1
DEVICE_IN=/dev/$BOARD # This is the device to program
DEVICE_OUT=/dev/$BOARD # This is what the device will be called after programming
FILE=bin/$BOARD.bin
PORT=USB1
# PROGRAMMER=~/local/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI
PROGRAMMER=~/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI

if [ $# -gt 1 ]; then
	DEVICE_IN=/dev/$2 # Device will change id after programming
fi

if [ $# -gt 2 ]; then
	PORT=$3 # Use a different port, e.g. SWD
fi

if [ ! -c $DEVICE_IN ]; then
	echo "Device $DEVICE_IN not found"
	exit 1
fi

# Get the device into bootloader mode
echo "O" > $DEVICE_IN

# wait for device to get into bootloader mode
sleep 1

$PROGRAMMER -c port=$PORT -w $FILE 0x8000000 --start || exit 1

elapsed=0
timeout=50 # 5 seconds
while true; do
	if [ -c $DEVICE_OUT ]; then
		echo "Success"
		exit 0
	fi
	if [ $elapsed -eq $timeout ]; then
		echo "Failed"
		exit 1
	fi
	((elapsed=elapsed+1))
	sleep 0.1
done
