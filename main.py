from genericpath import isfile

import search_util_v2 as search_v2
from pathlib import Path

from datetime import datetime

# input_key = input("输入要查找的Key:")
# input_value = input("输入要查找的Value:")

json_folder = Path("./json")

now = datetime.now()

time_str = now.strftime("%Y-%m-%d-%H-%M-%S")

log_path = f"logs\\{time_str}.txt"

elapsed = 0
total_elapsed = 0

for path in json_folder.iterdir():
    if path.glob("*.py"):
        with open(path, "r") as f:
            elapsed = search_v2.search_by_key(f, "id", log_path)
            # search.search_by_key_v2(f, "uid")
    total_elapsed += elapsed


print(f"耗时: {elapsed:.1f} 秒")
    