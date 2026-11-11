import csv
import os
import subprocess
import sys
from pathlib import Path

import pytest

from notes import (
    export_csv,
    find_files,
    find_md_files,
    normalize_exts,
    scan_folder,
    search_keyword,
)

MAIN = Path(__file__).parent / "main.py"


@pytest.fixture
def notes_dir(tmp_path):
    for name in ["a.md", "b.txt", "d.py"]:
        (tmp_path / name).write_text("AI\n", encoding="utf-8")
    return tmp_path


def names(paths):
    return sorted(Path(p).name for p in paths)


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(MAIN), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )


# ---- normalize_exts ----

def test_normalize_adds_dot():
    assert normalize_exts(["txt"]) == (".txt",)


def test_normalize_lowercase_and_dedupe():
    assert normalize_exts([".MD", "md", "txt", ".txt"]) == (".md", ".txt")


@pytest.mark.parametrize("bad", [[""], ["."], []])
def test_normalize_rejects_empty(bad):
    with pytest.raises(ValueError):
        normalize_exts(bad)


# ---- find_files / scan_folder ----

def test_default_only_md(notes_dir):
    assert names(find_files(str(notes_dir))) == ["a.md"]
    assert names(find_md_files(str(notes_dir))) == ["a.md"]


def test_multiple_exts(notes_dir):
    assert names(find_files(str(notes_dir), [".md", ".txt"])) == ["a.md", "b.txt"]


def test_ext_without_dot(notes_dir):
    assert names(find_files(str(notes_dir), ["txt"])) == ["b.txt"]


def test_ext_case_insensitive(notes_dir):
    (notes_dir / "E.TXT").write_text("AI\n", encoding="utf-8")
    assert names(find_files(str(notes_dir), ["txt"])) == ["E.TXT", "b.txt"]


def test_ext_recurses_subfolders(notes_dir):
    sub = notes_dir / "sub"
    sub.mkdir()
    (sub / "c.txt").write_text("AI\n", encoding="utf-8")
    assert names(find_files(str(notes_dir), ["txt"])) == ["b.txt", "c.txt"]


def test_scan_folder_with_exts(notes_dir):
    results = scan_folder(str(notes_dir), [".md", ".txt"])
    assert names(p for p, _ in results) == ["a.md", "b.txt"]


# ---- search / CSV ----

def test_search_with_exts(notes_dir):
    results = search_keyword(str(notes_dir), "AI", [".md", ".txt"])
    assert names(p for p, _, _ in results) == ["a.md", "b.txt"]


def test_csv_export_with_exts(notes_dir, tmp_path):
    output = tmp_path / "out.csv"
    export_csv(search_keyword(str(notes_dir), "AI", ["md", "txt"]), str(output))
    with output.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    assert names(row[0] for row in rows[1:]) == ["a.md", "b.txt"]


# ---- CLI (验收标准) ----

def test_cli_default(notes_dir):
    r = run_cli("--folder", str(notes_dir))
    assert r.returncode == 0, r.stderr
    assert "文件数：1，" in r.stdout


def test_cli_multiple_exts(notes_dir):
    r = run_cli("--folder", str(notes_dir), "--ext", ".md", ".txt")
    assert r.returncode == 0, r.stderr
    assert "文件数：2，" in r.stdout


def test_cli_search_multiple_exts(notes_dir):
    r = run_cli("--folder", str(notes_dir), "--ext", ".md", ".txt", "--keyword", "AI")
    assert r.returncode == 0, r.stderr
    assert "a.md:1: AI" in r.stdout
    assert "b.txt:1: AI" in r.stdout
    assert "d.py" not in r.stdout


def test_cli_ext_without_dot(notes_dir):
    r = run_cli("--folder", str(notes_dir), "--ext", "txt")
    assert r.returncode == 0, r.stderr
    assert "文件数：1，" in r.stdout


def test_cli_invalid_ext(notes_dir):
    r = run_cli("--folder", str(notes_dir), "--ext", ".")
    assert r.returncode == 2


def test_cli_output_requires_keyword(notes_dir, tmp_path):
    r = run_cli("--folder", str(notes_dir), "--output", str(tmp_path / "x.csv"))
    assert r.returncode == 2
