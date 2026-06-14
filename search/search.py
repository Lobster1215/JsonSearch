import mmap
import time
from typing import IO
import utils.mmap_utils as mmap_util

def search_test(f: IO, k: str, log_path: str):
    
    start_time = time.time()

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
        match_count += 1

        key_start = mm.find(
            key_pattern,
            key_start + len(key_pattern)
        )
    elapsed = time.time() - start_time
    return elapsed, match_count 

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
    mm_len = len(mm)
    key_b = k.encode("utf-8")
    key_pattern = b'"' + key_b + b'"'  # 带引号搜索，避免匹配子串如 "valid" 中的 "id"
    match_count = 0
    key_start = mm.find(key_pattern)
    while key_start >= 0:
        key_end = key_start + len(key_pattern) - 1  # 闭合引号位置
        
        is_key, pos = mmap_util.is_json_key(mm, key_end, mm_len)

        # 搜到不是Key的情况
        if not is_key:
            key_start = mm.find(
                key_pattern,
                key_start + len(key_pattern)
            )
            continue

        obj = mmap_util.parse_value(mm, pos)

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

    mm_len = len(mm)

    key_b = k.encode('utf-8')
    match_count = 0
    key_start = mm.find(key_b)
    is_key = False
    while key_start >= 0:
        key_end = mmap_util.find_str_end(mm, key_start + 1)
        
        is_key, pos = mmap_util.is_json_key(mm, key_end, mm_len)

        if not is_key:
            key_start = mm.find(
                key_b, 
                pos + len(key_b)
            )
            continue

        obj = mmap_util.parse_value(mm, pos)
        match_count += 1

        key_str = mm[key_start: key_end].decode("utf-8", errors="replace")
        val_str = obj.get('value').decode("utf-8", errors="replace") if obj.get('value') else ""
        f_log.write(f"file: {f_name}, key: {key_str}, offset: {key_start}, value: {val_str}\n")
        key_start = mm.find(key_b, obj.get("value_end"))

    f_log.close()
    mm.close()

    elapsed = time.time() - start_time

    return elapsed, match_count