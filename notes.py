from pathlib import Path
import csv

DEFAULT_EXTS = (".md",)


def normalize_exts(exts) -> tuple[str, ...]:
    """规范化扩展名：补齐前导点、转小写、去重（保持顺序）。空值或只有点时报错。"""
    result = []
    for ext in exts:
        ext = ext.strip().lower()
        if not ext.startswith("."):
            ext = "." + ext
        if ext == ".":
            raise ValueError("扩展名不能为空。")
        if ext not in result:
            result.append(ext)
    if not result:
        raise ValueError("至少需要一个扩展名。")
    return tuple(result)


def find_files(folder: str, exts=DEFAULT_EXTS) -> list[str]:
    """返回 folder 及其子文件夹里扩展名在 exts 中的所有文件路径（不区分大小写）。"""
    exts = normalize_exts(exts)
    return sorted(
        str(p) for p in Path(folder).rglob("*")
        if p.is_file() and p.name.lower().endswith(exts)
    )


def find_md_files(folder: str) -> list[str]:
    """返回 folder 及其子文件夹里所有 .md 文件的路径。"""
    return find_files(folder, DEFAULT_EXTS)


def read_text(path: str) -> str | None:
    for encoding in ["utf-8-sig", "gbk"]:
        try:
            return Path(path).read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return None

import re

WORD_PATTERN = re.compile(r"[\u4e00-\u9fff]|[0-9]|[A-Za-z]+")


def count_words(text: str) -> int:
    """统计字数：汉字、数字每个算 1，连续英文字母算 1 个单词，标点空白不算。"""
    return len(WORD_PATTERN.findall(text))

def scan_folder(folder: str, exts=DEFAULT_EXTS) -> list[tuple[str, int]]:
    """扫描文件夹，返回每个可读的指定扩展名文件的 (路径, 字数)；读不出的跳过并提示。"""
    results = []
    paths = find_files(folder, exts)
    texts = [read_text(path) for path in paths]
    for(path, text) in zip(paths, texts):
        if text is None:
            print(f"无法读取文件：{path}")
            continue
        results.append((path, count_words(text)))
    return results

def print_summary(results: list[tuple[str, int]]) -> None:
    """输出文件数和总字数。"""
    total_files = len(results)
    total_words = sum(word_count for _, word_count in results)
    print(f"文件数：{total_files}，总字数：{total_words}")

def search_keyword(folder: str, keyword: str, exts=DEFAULT_EXTS) -> list[tuple[str, int, str]]:
    keyword = keyword.lower().strip()
    if not keyword:
        raise ValueError("Keyword cannot be empty.")
    results = []
    paths = find_files(folder, exts)
    for path in paths:
        text = read_text(path)
        if(text is None):
            print(f"无法读取文件：{path}")
            continue
        else:
            lines = text.splitlines()
            for line_number, line in enumerate(lines, start=1):
                if keyword in line.lower():
                    results.append((path, line_number, line))
    return results


def export_csv(
    results: list[tuple[str, int, str]],
    output_path: str
) -> None:
    with open(output_path, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["文件路径", "行号", "匹配内容"])
        writer.writerows(results)