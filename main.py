from notes import scan_folder, print_summary,search_keyword
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Markdown 笔记整理工具")
parser.add_argument("--folder", required=True, help="要扫描的笔记文件夹")
parser.add_argument("--keyword", required=True, help="要搜索的关键词")
args = parser.parse_args()

if not Path(args.folder).is_dir():
    parser.error(f"不是有效的文件夹：{args.folder}")


FOLDER = args.folder


results = scan_folder(FOLDER)
print_summary(results)
keyword = args.keyword
try:
    tuples = search_keyword(FOLDER, keyword)
    if tuples:
        for path, line_number in tuples:
            print(f"{path}:{line_number}")
    else:
        print("未找到包含关键字的行。")
except ValueError as e:
    print(e)