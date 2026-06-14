import ijson
from typing import IO
from datetime import datetime

def search_by_key(f: IO, key):
    for item in ijson.items(f, "item"):
        for k in item:
            if k == key:
                print(k,"=",item[k])
                
def search_by_key_and_value(f: IO, key: str, value: str):
    for item in ijson.items(f, "item"):
        if str(item[key]) == value:
            pos = f.tell()
            print("pos:", pos, "", key, "=", value)

def search_by_key_v2(f: IO, k: str):
    
    # now = datetime.now()
    # time_str = now.strftime("%Y-%m-%d-%H-%M-%S")
    # log = open(f"logs\\{time_str}.txt", "w+")
    for prefix, event, value in ijson.parse(f):
       pos = f.tell()
       print("pos:", pos)
       print("prefix:", prefix)
       print("event:", event)
       print("value:", value)
       print("---------------")