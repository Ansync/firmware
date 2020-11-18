#!/usr/bin/python3

import signal, os

def handler(signum, frame):
    raise IOError("Timedout!")

def startTimer(seconds):
    # Set the signal handler and an alarm
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(seconds)

def stopTimer():
    # Disable the alarm
    signal.alarm(0)
