#!/usr/bin/python3

import redis
import timeout
import versions
import shell

VERSION_R = "8006"

r = redis.Redis(host='localhost', port=6379, db=0)

def reqVersion(board):
    r.publish(board, VERSION_R + 'r')

def parseVersion(msg):
    last = msg[len(msg) - 1]
    # only care about updates
    #  if chr(last) != 'u':
        #  return None
    arr = msg.split(b' ')
    # convert string to bytes string
    reg = bytes(VERSION_R, 'utf-8')
    # only care about version register
    if arr[0] != reg:
        return None
    # cut off last char "u"
    #  ver = arr[1][:-1]
    # convert hex string to int
    #  ver = int(ver, 16)
    ver = int(arr[1], 16)
    return ver

def waitForVersion(sub):
    for msg in sub.listen():
        data = msg['data']
        # check if bytes object or int
        if type(data) is not bytes:
            continue
        #  print(data)
        ver = parseVersion(data)
        # When version reg found, version number is returned
        if ver is None:
            continue
        return ver

def getVersion(board):
    # subscribe to board channel
    sub = r.pubsub()
    sub.subscribe("up/" + board)
    # request version
    reqVersion(board)
    # start timer to wake us from blocking listen()
    timeout.startTimer(5)
    ver = None
    try:
        # loop until version received or timeout
        ver = waitForVersion(sub)
    except:
        print("timedout wating for response")
    else:
        # success
        timeout.stopTimer()
        print(board, "version", ver)
    sub.unsubscribe(board)
    return ver

def enterBootloader(board):
    r.publish(board, 'O')

def checkVersions():
    # do a git pull to get latest fw versions
    shell.doPull()
    # load json with all board versions
    expected_version = versions.get()
    actual_version = {}
    upToDate = {}
    needsUpdate = {}
    for board in expected_version:
        ver = getVersion(board)
        if ver == None:
            print("Error getting version from", board)
            continue
        actual_version[board] = getVersion(board)
        if actual_version[board] < expected_version[board]:
            needsUpdate[board] = expected_version[board]
            enterBootloader(board)
            # Wait for device to enter bootloader
            sleep(1)
            shell.update(board)
        else:
            upToDate[board] = actual_version[board]
    print("needs update", needsUpdate)
    print("up-to-date", upToDate)

# If called as submodule name will be name of this script
if __name__ == "__main__":
    checkVersions()
