import pyperclip
import black
import ast
import time
import threading

from tkinter import messagebox, Tk

def is_valid_python(code):
    """語法合法性檢查"""
    try:
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, f"{e.msg}（第 {e.lineno} 行，第 {e.offset} 字元）"

def try_format_clipboard(prev_clip):
    code = pyperclip.paste()
    if code == prev_clip:
        return prev_clip  # 沒有改變

    if not code.strip():
        return code  # 忽略空白

    is_valid, err = is_valid_python(code)
    if not is_valid:
        print(f"❌ 非合法 Python 語法：{err}")
        return code

    try:
        formatted = black.format_str(code, mode=black.FileMode())
        pyperclip.copy(formatted)
        print("✅ 代碼已自動格式化並複製")
        return formatted
    except Exception as e:
        print(f"❌ 格式化錯誤：{str(e)}")
        return code

def clipboard_watcher():
    prev_content = pyperclip.paste()
    print("📋 自動格式化工具正在運行中... 請複製 Python 代碼")
    while True:
        try:
            prev_content = try_format_clipboard(prev_content)
        except Exception as e:
            print(f"錯誤：{e}")
        time.sleep(1)  # 每秒偵測一次

if __name__ == "__main__":
    # 非GUI版就不顯示視窗，但保留提示功能
    root = Tk()
    root.withdraw()  # 隱藏主視窗
    threading.Thread(target=clipboard_watcher, daemon=True).start()
    messagebox.showinfo("已啟動", "🟢 自動格式化工具正在背景運作，請開始複製程式碼。")
    root.mainloop()
