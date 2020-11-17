#!/usr/bin/python3

import json

PATH = "../versions.json"

def get():
# using the with statement makes sure the file is automatically closed after we
# are done with it, r+ means read and write
    with open(PATH, 'r') as f:
        obj = json.load(f)
        print(obj)
        return obj

# If called as submodule name will be name of this script
if __name__ == "__main__":
    get()
