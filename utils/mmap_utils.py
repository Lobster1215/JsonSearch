import mmap

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

        if pos == -1:  # 未找到闭合引号
            return len(mm)
        
        if mm[pos - 1:pos] != b'\\':
            return pos
        
        pos += 1

# 处理找到的Key对应的值
def parse_value(mm: mmap, value_start: int):
    i = value_start

    value_end = -1

    if mm[i:i+4] == b"true": # 布尔值处理
        value_end = i + 4
    elif mm[i:i+5] == b"false":
        value_end = i + 5
    elif mm[i:i+4] == b"null": # 空值处理
        value_end = i + 4
    elif mm[i:i+1] == b'"': # 字符串情况处理
        value_end = find_str_end(mm, i + 1) + 1
    elif mm[i:i+1] == b'[': # 数组情况处理
        value_end = find_bracket_end(mm, i + 1, '[', ']')
    elif mm[i:i+1] == b'{': # json情况处理
        value_end = find_bracket_end(mm, i + 1, '{', '}')
    else:
        # 数字情况处理（支持负数、小数、科学计数法）
        while mm[i:i+1] in b'0123456789.eE+-':
            i += 1
        value_end = i
    if value_end < 0:
        value_end = value_start

    return {
        "value": mm[value_start:value_end],
        "value_end": value_end
    }
