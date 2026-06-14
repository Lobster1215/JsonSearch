# JsonSearch

基于 `mmap`（内存映射文件）的高性能 JSON Key 搜索工具，适用于大型 JSON 文件（800MB ~ 2GB+）的快速检索。

## 项目结构

```
JsonSearch/
├── main.py                  # 入口文件，命令行参数解析与调度
├── search/
│   └── search.py            # 搜索逻辑（精确匹配 / 模糊匹配）
├── utils/
│   └── mmap_utils.py        # mmap 底层工具函数（值解析、括号匹配等）
├── generate_test_json.py    # 测试数据生成脚本
├── json/                    # 默认 JSON 文件存放目录
├── logs/                    # 搜索结果日志输出目录
└── tests/                   # 测试用例
```

## 使用方法

### 基本用法

```bash
python main.py -k <key>
```

### 完整参数

| 参数 | 缩写 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--key` | `-k` | ✅ | — | 要搜索的 JSON Key 名称 |
| `--dir` | `-d` | ❌ | `./json` | JSON 文件所在目录 |
| `--output` | `-o` | ❌ | `logs/<时间戳>.txt` | 日志输出文件路径 |
| `--recursive` | `-r` | ❌ | `false` | 是否递归搜索子目录 |
| `--mode` | `-m` | ❌ | `exact` | 搜索模式：`exact`（精确）/ `fuzzy`（模糊） |

### 使用示例

```bash
# 在默认目录中精确搜索 key 为 "id" 的字段
python main.py -k "id"

# 指定目录搜索
python main.py -k "name" -d ./data

# 指定日志输出路径
python main.py -k "uid" -o result.txt

# 递归搜索子目录
python main.py -k "id" -d ./json -r

# 模糊匹配（匹配包含目标字符串的所有 key）
python main.py -k "name" -m fuzzy
```

## 搜索模式

- **精确模式（`exact`）**：匹配完整的 JSON Key，例如搜索 `id` 只匹配 `"id"`，不会匹配 `"uid"` 或 `"valid"`。
- **模糊模式（`fuzzy`）**：匹配包含目标字符串的 Key，例如搜索 `id` 会匹配 `"id"`、`"uid"`、`"valid"` 等。

## 输出说明

搜索结果会同时输出到控制台和日志文件。

**控制台输出示例：**
```
搜索 Key: "uid"                                                                  
搜索目录: D:\DevProjects\JsonSearch\json
文件数量: 1
日志路径: logs\2026-06-14-13-49-32.txt
--------------------------------------------------
  test_large.json: 5484868 个匹配, 耗时 25.916s
--------------------------------------------------
总计: 5484868 个匹配, 耗时 25.916s
```

**日志文件格式：**
```
file: json\manifest.spdx.json, key: SPDXID, offset: 149, value: "SPDXRef-Package-xxx"
```

每条记录包含：文件名、匹配的 Key、字节偏移量、对应的 Value。

## 生成测试数据

项目附带测试数据生成脚本，可创建大型 JSON 文件用于性能测试：

```bash
python generate_test_json.py
```

默认生成 1GB 的测试文件，可在脚本中修改 `TARGET_SIZE_MB` 参数调整大小。

## 性能特点

- 使用 `mmap` 内存映射读取文件，避免将整个文件加载到内存
- 直接在字节层面搜索，无需 JSON 解析，速度极快
- 适用于 GB 级别的大型 JSON 文件