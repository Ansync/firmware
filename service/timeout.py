#!/usr/bin/python3

import signal, os

def handler(signum, frame):
    raise IOError("Timedout!")

def startTimer(seconds):
    # Set alarm
    signal.alarm(seconds)

def stopTimer():
    # Disable the alarm
    signal.alarm(0)

# Set the signal handler
signal.signal(signal.SIGALRM, handler)
