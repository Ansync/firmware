#!/bin/bash

if [ $# -lt 1 ]; then
	echo "Need to specify a board"
	exit 1
fi

BOARD=$1
DEVICE_OUT=/dev/$BOARD # This is what the device will be called after programming
FILE=bin/$BOARD.bin
PORT=SWD
# PROGRAMMER=~/local/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI
PROGRAMMER=~/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI

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
