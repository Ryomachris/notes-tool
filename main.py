from notes import scan_folder, print_summary, search_keyword, export_csv, normalize_exts
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Markdown 笔记整理工具")
parser.add_argument("--folder", required=True, help="要扫描的笔记文件夹")
parser.add_argument("--keyword", help="要搜索的关键词（不传时只输出统计）")
parser.add_argument("--output", help="CSV 导出文件路径（需配合 --keyword）")
parser.add_argument(
    "--ext",
    nargs="+",
    default=[".md"],
    help="要扫描的扩展名，可传多个，如 --ext .md .txt；不带点会自动补齐；默认 .md",
)
args = parser.parse_args()

if not Path(args.folder).is_dir():
    parser.error(f"不是有效的文件夹：{args.folder}")
if args.output and args.keyword is None:
    parser.error("--output 需要配合 --keyword 使用")
try:
    exts = normalize_exts(args.ext)
except ValueError as e:
    parser.error(f"--ext 参数无效：{e}")


FOLDER = args.folder


results = scan_folder(FOLDER, exts)
print_summary(results)
keyword = args.keyword
if keyword is not None:
    try:
        tuples = search_keyword(FOLDER, keyword, exts)
        if tuples:
            for path, line_number, line in tuples:
                print(f"{path}:{line_number}: {line}")
        else:
            print("未找到包含关键字的行。")
        if args.output:
            export_csv(tuples, args.output)
            print(f"搜索结果已导出到：{args.output}")
    except ValueError as e:
        print(e)
