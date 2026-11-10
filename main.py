from notes import scan_folder, print_summary,search_keyword

FOLDER = "C:/projs/notes-tool/test_notes"


results = scan_folder(FOLDER)
print_summary(results)
keyword = input("请输入要搜索的关键字：")
try:
    tuples = search_keyword(FOLDER, keyword)
    if tuples:
        for path, line_number in tuples:
            print(f"{path}:{line_number}")
    else:
        print("未找到包含关键字的行。")
except ValueError as e:
    print(e)