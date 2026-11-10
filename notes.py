from pathlib import Path
import csv

def find_md_files(folder: str) -> list[str]:
    # 你来写：返回 folder 及其子文件夹里所有 .md 文件的路径
    dad_path = Path(folder)
    return sorted(str(p) for p in dad_path.rglob("*.md"))


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

def scan_folder(folder: str) -> list[tuple[str, int]]:
    """扫描文件夹，返回每个可读 .md 文件的 (路径, 字数)；读不出的跳过并提示。"""
    results = []
    paths = find_md_files(folder)
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

def search_keyword(folder: str,keyword: str) -> list[tuple[str, int, str]]:
    keyword = keyword.lower().strip()
    if not keyword:
        raise ValueError("Keyword cannot be empty.")
    results = []
    paths = find_md_files(folder)
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