"""
Setup and management script for Google Calendar Hotkey Autostart
"""

import os
import sys
import winreg

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_SCRIPT = os.path.join(SCRIPT_DIR, "google_calendar_toggle.pyw")
STARTUP_DIR = os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs\Startup")
VBS_PATH = os.path.join(STARTUP_DIR, "GoogleCalendarHotkey.vbs")
REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME = "GoogleCalendarHotkey"

def get_pythonw():
    pythonw = sys.executable.replace("python.exe", "pythonw.exe")
    if os.path.exists(pythonw):
        return pythonw
    return sys.executable

def install():
    pythonw = get_pythonw()
    cmd = f'"{pythonw}" "{MAIN_SCRIPT}"'
    
    # 1. Register in Registry
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_ALL_ACCESS) as key:
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, cmd)
        print("[OK] Đã đăng ký Registry Run.")
    except Exception as e:
        print(f"[!] Lỗi đăng ký Registry: {e}")

    # 2. Create VBS launcher in Startup folder
    try:
        if os.path.exists(STARTUP_DIR):
            vbs_content = (
                'Set WshShell = CreateObject("WScript.Shell")\n'
                f'WshShell.Run """{pythonw}"" ""{MAIN_SCRIPT}""", 0, False\n'
            )
            with open(VBS_PATH, "w", encoding="utf-8") as f:
                f.write(vbs_content)
            print(f"[OK] Đã tạo file khởi động ngầm: {VBS_PATH}")
    except Exception as e:
        print(f"[!] Lỗi tạo file Startup: {e}")

    print("\n==> Tự động khởi động cùng Windows: ĐÃ KÍCH HOẠT THÀNH CÔNG!")

def uninstall():
    # 1. Remove from Registry
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_ALL_ACCESS) as key:
            try:
                winreg.DeleteValue(key, APP_NAME)
                print("[OK] Đã xóa khỏi Registry Run.")
            except FileNotFoundError:
                print("[i] Không tìm thấy khóa Registry.")
    except Exception as e:
        print(f"[!] Lỗi xóa Registry: {e}")

    # 2. Remove VBS from Startup folder
    try:
        if os.path.exists(VBS_PATH):
            os.remove(VBS_PATH)
            print("[OK] Đã xóa file khởi động trong Startup.")
    except Exception as e:
        print(f"[!] Lỗi xóa file Startup: {e}")

    print("\n==> Tự động khởi động cùng Windows: ĐÃ HỦY THÀNH CÔNG!")

def status():
    reg_ok = False
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ) as key:
            val, _ = winreg.QueryValueEx(key, APP_NAME)
            reg_ok = bool(val)
    except Exception:
        reg_ok = False

    vbs_ok = os.path.exists(VBS_PATH)
    print(f"Trạng thái Registry Run: {'BẬT' if reg_ok else 'TẮT'}")
    print(f"Trạng thái Startup Folder: {'BẬT' if vbs_ok else 'TẮT'}")
    return reg_ok or vbs_ok

if __name__ == "__main__":
    action = sys.argv[1].lower() if len(sys.argv) > 1 else "install"
    if action == "install":
        install()
    elif action == "uninstall":
        uninstall()
    elif action == "status":
        status()
    else:
        print(f"Lệnh không hợp lệ: {action}. Dùng 'install', 'uninstall', hoặc 'status'.")
