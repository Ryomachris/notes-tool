import csv
from pathlib import Path
from tempfile import TemporaryDirectory

from notes import export_csv


with TemporaryDirectory() as folder:
    output = Path(folder) / "test.csv"

    data = [("note.md", 3, "AI, Python")]
    export_csv(data, str(output))

    with output.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.reader(file))

    assert rows == [
        ["文件路径", "行号", "匹配内容"],
        ["note.md", "3", "AI, Python"],
    ]

print("CSV 导出测试通过")