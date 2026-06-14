import mmap
import time
from typing import IO
import utils.mmap_utils as mmap_util

# 通过Key精确查找
def search_by_key(f: IO, k: str, log_path: str):
    f_name = f.name
    start_time = time.time()
    f_log = open(log_path, "a", encoding="utf-8") # 日志 会将找到的Key输出到日志中

    mm = mmap.mmap(
        f.fileno(),
        0,
        access=mmap.ACCESS_READ
    )

    key_b = k.encode("utf-8")
    key_pattern = b'"' + key_b + b'"'  # 带引号搜索，避免匹配子串如 "valid" 中的 "id"
    match_count = 0
    key_start = mm.find(key_pattern)
    while key_start >= 0:
        key_end = key_start + len(key_pattern) - 1  # 闭合引号位置
        colon = mm.find(b":", key_end) # Key后的冒号
        i = colon + 1
        while mm[i:i+1] in b'\t\n\r ': # 处理冒号后的空格等不可见元素
            i += 1
        
        obj = mmap_util.parse_value(mm, i)
        match_count += 1

        key_str = mm[key_start+1:key_end].decode("utf-8", errors="replace")
        val_str = obj.get('value').decode("utf-8", errors="replace") if obj.get('value') else ""
        f_log.write(f"file: {f_name}, key: {key_str}, offset: {key_start}, value: {val_str}\n")
        key_start = mm.find(key_pattern, obj.get("value_end"))
        
    f_log.close()
    mm.close()

    elapsed = time.time() - start_time

    return elapsed, match_count 

def search_funzzy_key(f: IO, k: str, log_path: str):
    f_name = f.name
    f_log = open(log_path, 'a', encoding='utf-8')
    start_time = time.time()

    mm = mmap.mmap(
        f.fileno(),
        0,
        access=mmap.ACCESS_READ
    )

    key_b = k.encode('utf-8')
    match_count = 0
    key_start = mm.find(key_b)
    while key_start >= 0:
        key_end = mmap_util.find_str_end(mm, key_start + 1)
        colon = mm.find(b":", key_end)
        i = colon + 1
        while mm[i:i+1] in b'\t\n\r ':
            i += 1

        obj = mmap_util.parse_value(mm, i)
        match_count += 1

        key_str = mm[key_start: key_end].decode("utf-8", errors="replace")
        val_str = obj.get('value').decode("utf-8", errors="replace") if obj.get('value') else ""
        f_log.write(f"file: {f_name}, key: {key_str}, offset: {key_start}, value: {val_str}\n")
        key_start = mm.find(key_b, obj.get("value_end"))

    f_log.close()
    mm.close()

    elapsed = time.time() - start_time

    return elapsed, match_count