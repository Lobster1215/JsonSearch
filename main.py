import argparse
import sys
import search.search as search
from pathlib import Path
from datetime import datetime


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="JSON Key 搜索工具 — 基于 mmap 的高性能大文件搜索"
    )
    parser.add_argument(
        "-k", "--key",
        type=str,
        required=True,
        help="要搜索的 JSON Key 名称 (如: id, name, uid)"
    )
    parser.add_argument(
        "-d", "--dir",
        type=str,
        default="./json",
        help="JSON 文件所在目录 (默认: ./json)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="日志输出文件路径 (默认: logs/<时间戳>.txt)"
    )
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="是否递归搜索子目录"
    )
    parser.add_argument(
        "-m", "--mode",
        type=str,
        default="exact",
        help="搜索模式 默认精确搜索"
    )

    return parser.parse_args()


def collect_json_files(folder: Path, recursive: bool) -> list[Path]:
    """收集目录下的 JSON 文件"""
    if recursive:
        files = sorted(folder.rglob("*.json"))
    else:
        files = sorted(folder.glob("*.json"))
    return files


def main():
    args = parse_args()

    json_folder = Path(args.dir)
    if not json_folder.is_dir():
        print(f"错误: 目录不存在 — {json_folder}")
        sys.exit(1)

    # 确定日志路径
    if args.output:
        log_path = args.output
    else:
        time_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        log_path = f"logs\\{time_str}.txt"

    # 确保日志目录存在
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)

    # 收集 JSON 文件
    json_files = collect_json_files(json_folder, args.recursive)
    if not json_files:
        print(f"未在 {json_folder.resolve()} 中找到 JSON 文件")
        sys.exit(0)

    print(f"搜索 Key: \"{args.key}\"")
    print(f"搜索目录: {json_folder.resolve()}")
    print(f"文件数量: {len(json_files)}")
    print(f"日志路径: {log_path}")
    print("-" * 50)

    total_elapsed = 0.0
    total_matches = 0

    for path in json_files:
        try:
            with open(path, "r", encoding="utf-8") as f:
                elapsed = 0
                count = 0
                if args.mode == "fuzzy" :
                    elapsed, count = search.search_funzzy_key(f, args.key, log_path)
                else:
                    elapsed, count = search.search_by_key(f, args.key, log_path)
                total_elapsed += elapsed
                total_matches += count
                if count > 0:
                    print(f"  {path.name}: {count} 个匹配, 耗时 {elapsed:.3f}s")
        except Exception as e:
            print(f"  {path.name}: 处理失败 — {e}")

    print("-" * 50)
    print(f"总计: {total_matches} 个匹配, 耗时 {total_elapsed:.3f}s")


if __name__ == "__main__":
    main()