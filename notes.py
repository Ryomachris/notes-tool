from pathlib import Path


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