#!/usr/bin/python3

import redisClient
import update
import version
import json

def main():
    redis = redisClient.RedisClient()
    inCh = "update"
    outCh = "up/update"
    redis.subscribe("update")
    while True:
        data = redis.listen("update")
        if not data:
            continue
        if data == "checkAll":
            updateList = version.checkAll(redis)
            # Convert json to string and send upstream
            redis.publish(outCh, json.dumps(updateList))
        elif data == "updateAll":
            updateList = version.checkAll(redis)
            ret = 0
            for board in updateList:
                ret = ret + update.updateBoard(updateList[board])
            if ret:
                redis.publish(outCh, "failed")
            else:
                redis.publish(outCh, "success")
        else:
            # returns 0 if successful
            ret = update.updateBoard(data)
            if ret:
                redis.publish(outCh, "failed")
            else:
                redis.publish(outCh, "success")

main()
