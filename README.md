
# Markdown 笔记整理器

一个基于 Python 的命令行工具，用于管理和搜索 Markdown 笔记。

## 功能

- 递归扫描文件夹中的 `.md` 文件，也可通过 `--ext` 指定其他扩展名（如 `.txt`）
- 统计文件数量和总字数
- 根据关键词搜索笔记
- 显示匹配的文件路径、行号和内容
- 将搜索结果导出为 CSV 文件

## 运行环境

- Python 3.10 或更高版本
- 无须安装第三方依赖


## 使用方法

### 1. 搜索 Markdown 笔记

```powershell
python main.py --folder ./test_notes --keyword AI
```

程序会输出匹配的文件路径、行号和内容。

### 2. 导出搜索结果到 CSV

```powershell
python main.py --folder ./test_notes --keyword AI --output results.csv
```

搜索结果会保存到 `results.csv` 文件中。

### 3. 扫描其他扩展名

默认只扫描 `.md`。使用 `--ext` 可以指定一个或多个扩展名，统计、搜索和 CSV 导出都会生效：

```powershell
# 同时扫描 .md 和 .txt
python main.py --folder ./test_notes --ext .md .txt --keyword AI

# 不带点也可以，会自动补成 .txt
python main.py --folder ./test_notes --ext txt
```

不传 `--keyword` 时只输出文件数和总字数。

### 4. 查看帮助

```powershell
python main.py --help
```

## 运行测试

项目运行本身不需要第三方依赖，但运行自动化测试需要安装 pytest。

安装测试依赖：

```powershell
python -m pip install pytest
```

运行测试：

```powershell
python -m pytest -v
```

## 注意事项

- `--folder`：要扫描的笔记文件夹路径。
- `--keyword`：可选参数，要搜索的关键词；不传时只输出统计信息。
- `--output`：可选参数，指定 CSV 输出路径，需要配合 `--keyword` 使用。
- `--ext`：可选参数，要扫描的扩展名，可传多个（如 `--ext .md .txt`）；不带点会自动补齐，不区分大小写；默认 `.md`。
- 可以将 `./test_notes` 替换为自己的笔记文件夹路径。
- 已存在的 CSV 输出文件会被覆盖。

