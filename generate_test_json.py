"""
生成大型 JSON 测试文件 (800MB ~ 2GB)
用于测试 search_util_v2.py 的 mmap 搜索工具
"""

import json
import random
import string
import time
import os

# ============ 配置 ============
TARGET_SIZE_MB = 1024  # 目标文件大小 (MB)，可在 800~2048 之间调整
OUTPUT_FILE = ".\\json\\test_large.json"
SEPARATOR = ",\n"  # JSON 元素之间的分隔符

# ============ 数据池 ============
FIRST_NAMES = [
    "Tom", "Jerry", "Kimi", "Kevin", "Tim", "Uber", "Alice", "Bob",
    "Charlie", "David", "Eve", "Frank", "Grace", "Hank", "Ivy", "Jack",
    "Kate", "Leo", "Mia", "Noah", "Olivia", "Peter", "Quinn", "Rose",
    "Sam", "Tina", "Uma", "Vince", "Wendy", "Xavier", "Yuki", "Zoe",
    "张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十",
    "欧阳锋", "黄药师", "洪七公", "段誉", "乔峰", "虚竹", "令狐冲",
    "任盈盈", "岳不群", "风清扬", "张无忌", "赵敏", "周芷若", "小龙女",
    "杨过", "郭靖", "黄蓉", "萧远山", "慕容博", "鸠摩智", "游坦之",
]

LAST_NAMES = ["", "", "", "", " Smith", " Johnson", " Lee", " Wang", " Li", " Zhang",
              " Chen", " Yang", " Huang", " Liu", " Wu", " Zhou"]


def random_string(min_len=3, max_len=15):
    length = random.randint(min_len, max_len)
    return "".join(random.choices(string.ascii_lowercase, k=length))


def generate_one_item(uid: int) -> dict:
    name = random.choice(FIRST_NAMES) + random.choice(LAST_NAMES)
    if random.random() < 0.3:
        name += "_" + random_string(4, 8)
    return {
        "uid": uid,
        "name": name,
        "level": random.randint(1, 100),
        "score": round(random.uniform(0, 1000), 2),
        "city": random.choice(["Beijing", "Shanghai", "Guangzhou", "Shenzhen",
                                "Hangzhou", "Chengdu", "Wuhan", "Nanjing",
                                "Xi'an", "Chongqing", "Suzhou", "Tianjin"]),
        "tags": [random_string(3, 8) for _ in range(random.randint(1, 5))],
        "description": " ".join(random_string(4, 10) for _ in range(random.randint(3, 8))),
    }


def format_item(item: dict) -> str:
    return json.dumps(item, ensure_ascii=False)


def main():
    target_bytes = TARGET_SIZE_MB * 1024 * 1024
    print(f"目标大小: {TARGET_SIZE_MB} MB ({target_bytes:,} bytes)")
    print(f"输出文件: {OUTPUT_FILE}")
    print()

    start_time = time.time()
    uid = 1000

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("[\n")

        bytes_written = f.tell()
        first = True

        while bytes_written < target_bytes:
            item = generate_one_item(uid)
            uid += 1

            line = format_item(item)
            if first:
                f.write("    " + line)
                first = False
            else:
                f.write(SEPARATOR + "    " + line)

            bytes_written = f.tell()

            # 进度显示
            if uid % 10000 == 0:
                pct = bytes_written / target_bytes * 100
                elapsed = time.time() - start_time
                speed = bytes_written / (1024 * 1024) / elapsed if elapsed > 0 else 0
                print(f"\r  进度: {pct:5.1f}% | "
                      f"已写入: {bytes_written / (1024*1024):.1f} MB | "
                      f"条数: {uid - 1000:,} | "
                      f"速度: {speed:.1f} MB/s", end="", flush=True)

        f.write("\n]\n")
        final_size = f.tell()

    elapsed = time.time() - start_time
    print()
    print()
    print(f"✅ 完成!")
    print(f"   文件: {OUTPUT_FILE}")
    print(f"   大小: {final_size / (1024*1024):.1f} MB ({final_size:,} bytes)")
    print(f"   条数: {uid - 1000:,}")
    print(f"   耗时: {elapsed:.1f} 秒")


if __name__ == "__main__":
    main()
