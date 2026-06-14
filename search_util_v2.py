import mmap
from re import I, S
from typing import IO
from datetime import datetime
import time

# 查找括号结尾
def find_bracket_end(mm: mmap, start: int, left_bracket: str, right_bracket: str):
    depth = 1
    pos = start + 1

    while pos < len(mm):
        c = mm[pos:pos + 1]

        if c == left_bracket.encode('utf-8'):
            depth += 1
        elif c == right_bracket.encode('utf-8'):
            depth -= 1

            if depth == 0:
                return pos + 1
            
        pos += 1

    return start

# 查找字符串结尾
def find_str_end(mm: mmap, start: int):
    pos = start + 1

    while pos < len(mm):
        pos = mm.find(b'"', pos)

        if mm[pos - 1:pos] != b'\\':
            return pos
        
        pos += 1

# 处理找到的Key对应的值
def value_handle(mm: mmap, value_start: int):
    i = value_start

    value_end = -1

    if mm[i:i+4] == b"true": # 布尔值处理
        value_end = i + 4
    elif mm[i:i+5] == b"false":
        value_end = i + 5
    elif mm[i:i+4] == b"null": # 空值处理
        value_end == i + 4
    elif mm[i:i+1] == b'"': # 字符串情况处理
        value_end = find_str_end(mm, i + 1)
    elif mm[i:i+1] == b'[': # 数组情况处理
        value_end = find_bracket_end(mm, i + 1, '[', ']')
    elif mm[i:i+1] == b'{': # json情况处理
        value_end = find_bracket_end(mm, i + 1, '{', '}')
    else:
        # 数字情况处理
        while mm[i:i+1] in b'0123456789':
            i += 1
        value_end = i
    if value_end < 0:
        value_end = value_start

    return {
        "value": mm[value_start:value_end],
        "value_end": value_end
    }

# 查找Key
def search_by_key(f:IO, k: str, log_path: str):
    f_name = f.name
    start_time = time.time()
    f_log = open(log_path, "a") # 日志 会将找到的Key输出到日志中

    mm = mmap.mmap(
        f.fileno(),
        0,
        access=mmap.ACCESS_READ
    )

    key_b = k.encode("utf-8")
    key_start = mm.find(key_b)
    while key_start > 0:
        key_end = mm.find(b'"', key_start) # 找Key闭合引号
        colon = mm.find(b":", key_end) # Key后的冒号
        i = colon + 1
        while mm[i:i+1] in b'\t\n\r ': # 处理冒号后的空格等不可见元素
            i += 1
        
        obj = value_handle(mm, i)

        f_log.write(f"file: {f_name}, key: {mm[key_start:key_end]}, offset: {key_start}, value: {obj.get('value')} \n")
        key_start = mm.find(key_b, obj.get("value_end"))
        
    
    f_log.close()
    mm.close()

    elapsed = time.time() - start_time

    return elapsed 
