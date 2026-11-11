
# Markdown 笔记整理器

一个基于 Python 的命令行工具，用于管理和搜索 Markdown 笔记。

## 功能

- 递归扫描文件夹中的 `.md` 文件
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

### 3. 查看帮助

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

- `--folder`：要扫描的 Markdown 文件夹路径。
- `--keyword`：要搜索的关键词。
- `--output`：可选参数，指定 CSV 输出路径。
- 可以将 `./test_notes` 替换为自己的笔记文件夹路径。
- 已存在的 CSV 输出文件会被覆盖。

