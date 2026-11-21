"""
Google Calendar Toggle & Autostart Utility for Windows
Tự động mở khi khởi động máy, ấn tổ hợp phím để hiện / ẩn Google Calendar.
"""

import sys
import os
import json
import time
import winreg
import threading
import subprocess
import ctypes
from ctypes import wintypes

# Ensure working directory is the script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")
ICON_FILE = os.path.join(SCRIPT_DIR, "calendar.ico")

# ----------------- Win32 API Definitions -----------------
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
shell32 = ctypes.windll.shell32

WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_longlong, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)
WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

class POINT(ctypes.Structure):
    _fields_ = [('x', wintypes.LONG), ('y', wintypes.LONG)]

class WNDCLASSEXW(ctypes.Structure):
    _fields_ = [
        ('cbSize', wintypes.UINT),
        ('style', wintypes.UINT),
        ('lpfnWndProc', WNDPROC),
        ('cbClsExtra', ctypes.c_int),
        ('cbWndExtra', ctypes.c_int),
        ('hInstance', wintypes.HINSTANCE),
        ('hIcon', wintypes.HICON),
        ('hCursor', wintypes.HICON),
        ('hbrBackground', wintypes.HBRUSH),
        ('lpszMenuName', wintypes.LPCWSTR),
        ('lpszClassName', wintypes.LPCWSTR),
        ('hIconSm', wintypes.HICON)
    ]

class NOTIFYICONDATAW(ctypes.Structure):
    _fields_ = [
        ('cbSize', wintypes.DWORD),
        ('hWnd', wintypes.HWND),
        ('uID', wintypes.UINT),
        ('uFlags', wintypes.UINT),
        ('uCallbackMessage', wintypes.UINT),
        ('hIcon', wintypes.HICON),
        ('szTip', wintypes.WCHAR * 128),
        ('dwState', wintypes.DWORD),
        ('dwStateMask', wintypes.DWORD),
        ('szInfo', wintypes.WCHAR * 256),
        ('uTimeoutOrVersion', wintypes.UINT),
        ('szInfoTitle', wintypes.WCHAR * 64),
        ('dwInfoFlags', wintypes.DWORD),
        ('guidItem', ctypes.c_byte * 16),
        ('hBalloonIcon', wintypes.HICON),
    ]

# Setup Win32 API types
user32.RegisterClassExW.argtypes = [ctypes.POINTER(WNDCLASSEXW)]
user32.RegisterClassExW.restype = wintypes.ATOM
user32.CreateWindowExW.argtypes = [
    wintypes.DWORD, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.DWORD,
    ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
    wintypes.HWND, wintypes.HMENU, wintypes.HINSTANCE, wintypes.LPVOID
]
user32.CreateWindowExW.restype = wintypes.HWND
user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
user32.DefWindowProcW.restype = ctypes.c_longlong
user32.DestroyWindow.argtypes = [wintypes.HWND]
user32.DestroyWindow.restype = wintypes.BOOL
user32.PostQuitMessage.argtypes = [ctypes.c_int]
user32.RegisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int, wintypes.UINT, wintypes.UINT]
user32.RegisterHotKey.restype = wintypes.BOOL
user32.UnregisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int]
user32.UnregisterHotKey.restype = wintypes.BOOL
user32.GetMessageW.argtypes = [ctypes.POINTER(wintypes.MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT]
user32.GetMessageW.restype = wintypes.BOOL
user32.TranslateMessage.argtypes = [ctypes.POINTER(wintypes.MSG)]
user32.TranslateMessage.restype = wintypes.BOOL
user32.DispatchMessageW.argtypes = [ctypes.POINTER(wintypes.MSG)]
user32.DispatchMessageW.restype = ctypes.c_longlong
user32.PostMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
user32.PostMessageW.restype = wintypes.BOOL

user32.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
user32.ShowWindow.restype = wintypes.BOOL
user32.IsWindow.argtypes = [wintypes.HWND]
user32.IsWindow.restype = wintypes.BOOL
user32.IsWindowVisible.argtypes = [wintypes.HWND]
user32.IsWindowVisible.restype = wintypes.BOOL
user32.IsIconic.argtypes = [wintypes.HWND]
user32.IsIconic.restype = wintypes.BOOL
user32.GetForegroundWindow.argtypes = []
user32.GetForegroundWindow.restype = wintypes.HWND
user32.SetForegroundWindow.argtypes = [wintypes.HWND]
user32.SetForegroundWindow.restype = wintypes.BOOL
user32.BringWindowToTop.argtypes = [wintypes.HWND]
user32.BringWindowToTop.restype = wintypes.BOOL
user32.AttachThreadInput.argtypes = [wintypes.DWORD, wintypes.DWORD, wintypes.BOOL]
user32.AttachThreadInput.restype = wintypes.BOOL
user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
user32.GetWindowThreadProcessId.restype = wintypes.DWORD
kernel32.GetCurrentThreadId.argtypes = []
kernel32.GetCurrentThreadId.restype = wintypes.DWORD
user32.keybd_event.argtypes = [ctypes.c_byte, ctypes.c_byte, wintypes.DWORD, ctypes.c_void_p]

user32.CreatePopupMenu.argtypes = []
user32.CreatePopupMenu.restype = wintypes.HMENU
user32.AppendMenuW.argtypes = [wintypes.HMENU, wintypes.UINT, ctypes.c_size_t, wintypes.LPCWSTR]
user32.AppendMenuW.restype = wintypes.BOOL
user32.TrackPopupMenu.argtypes = [
    wintypes.HMENU, wintypes.UINT, ctypes.c_int, ctypes.c_int,
    ctypes.c_int, wintypes.HWND, ctypes.c_void_p
]
user32.TrackPopupMenu.restype = ctypes.c_int
user32.DestroyMenu.argtypes = [wintypes.HMENU]
user32.DestroyMenu.restype = wintypes.BOOL
user32.GetCursorPos.argtypes = [ctypes.POINTER(POINT)]
user32.GetCursorPos.restype = wintypes.BOOL

user32.LoadImageW.argtypes = [
    wintypes.HINSTANCE, wintypes.LPCWSTR, wintypes.UINT,
    ctypes.c_int, ctypes.c_int, wintypes.UINT
]
user32.LoadImageW.restype = wintypes.HANDLE
user32.DestroyIcon.argtypes = [wintypes.HICON]
user32.DestroyIcon.restype = wintypes.BOOL
shell32.Shell_NotifyIconW.argtypes = [wintypes.DWORD, ctypes.POINTER(NOTIFYICONDATAW)]
shell32.Shell_NotifyIconW.restype = wintypes.BOOL

kernel32.CreateMutexW.argtypes = [ctypes.c_void_p, wintypes.BOOL, wintypes.LPCWSTR]
kernel32.CreateMutexW.restype = wintypes.HANDLE
kernel32.GetLastError.argtypes = []
kernel32.GetLastError.restype = wintypes.DWORD
kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
kernel32.CloseHandle.restype = wintypes.BOOL

user32.EnumWindows.argtypes = [WNDENUMPROC, wintypes.LPARAM]
user32.EnumWindows.restype = wintypes.BOOL
user32.GetClassNameW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
user32.GetClassNameW.restype = ctypes.c_int
user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
user32.GetWindowTextW.restype = ctypes.c_int
user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
user32.GetWindowTextLengthW.restype = ctypes.c_int

# Constants
WM_DESTROY = 0x0002
WM_USER = 0x0400
WM_TRAYICON = WM_USER + 20
WM_HOTKEY = 0x0312
WM_LBUTTONUP = 0x0202
WM_RBUTTONUP = 0x0205

NIM_ADD = 0x00000000
NIM_MODIFY = 0x00000001
NIM_DELETE = 0x00000002
NIF_MESSAGE = 0x00000001
NIF_ICON = 0x00000002
NIF_TIP = 0x00000004
NIF_INFO = 0x00000010
NIIF_INFO = 0x00000001

IMAGE_ICON = 1
LR_LOADFROMFILE = 0x00000010
LR_DEFAULTSIZE = 0x00000040

MF_STRING = 0x0000
MF_CHECKED = 0x0008
MF_UNCHECKED = 0x0000
MF_SEPARATOR = 0x0800
TPM_RIGHTBUTTON = 0x0002
TPM_RETURNCMD = 0x0100

MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004
MOD_WIN = 0x0008
MOD_NOREPEAT = 0x4000

HOTKEY_ID = 101

# Menu IDs
IDM_TOGGLE = 1001
IDM_LOGIN = 1002
IDM_AUTOSTART = 1003
IDM_OPEN_CONFIG = 1004
IDM_RELOAD = 1005
IDM_EXIT = 1006

# ----------------- Helper Functions -----------------

def parse_hotkey(hotkey_str):
    parts = [p.strip().lower() for p in hotkey_str.split('+')]
    mods = MOD_NOREPEAT
    key = None
    
    special_keys = {
        'space': 0x20, 'tab': 0x09, 'esc': 0x1B, 'escape': 0x1B,
        '`': 0xC0, '~': 0xC0, 'grave': 0xC0,
        'insert': 0x2D, 'delete': 0x2E, 'home': 0x24, 'end': 0x23,
        'pageup': 0x21, 'pagedown': 0x22,
    }
    for i in range(1, 25):
        special_keys[f'f{i}'] = 0x70 + i - 1

    for part in parts:
        if part in ('ctrl', 'control'):
            mods |= MOD_CONTROL
        elif part in ('alt',):
            mods |= MOD_ALT
        elif part in ('shift',):
            mods |= MOD_SHIFT
        elif part in ('win', 'windows'):
            mods |= MOD_WIN
        elif part in special_keys:
            key = special_keys[part]
        elif len(part) == 1:
            key = ord(part.upper())
        else:
            raise ValueError(f"Unknown key: {part}")
            
    if key is None:
        raise ValueError("No primary key found in hotkey string")
    return mods, key


def get_browser_executable(pref="auto"):
    edge_paths = [
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
        os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe'),
    ]
    chrome_paths = [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe'),
    ]
    firefox_paths = [
        r'C:\Program Files\Mozilla Firefox\firefox.exe',
        r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe',
        os.path.expandvars(r'%LOCALAPPDATA%\Mozilla Firefox\firefox.exe'),
    ]

    pref = pref.lower().strip()
    if pref == "edge":
        for p in edge_paths:
            if os.path.exists(p):
                return p, "edge"
    elif pref == "chrome":
        for p in chrome_paths:
            if os.path.exists(p):
                return p, "chrome"
    elif pref == "firefox":
        for p in firefox_paths:
            if os.path.exists(p):
                return p, "firefox"

    # Default / auto detection: Check Edge first (often has active MS/Windows profile), then Chrome
    for p in chrome_paths:
        if os.path.exists(p):
            return p, "chrome"
    for p in edge_paths:
        if os.path.exists(p):
            return p, "edge"
    for p in firefox_paths:
        if os.path.exists(p):
            return p, "firefox"

    return None, None


def is_autostart_registered():
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "GoogleCalendarHotkey"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ) as key:
            val, _ = winreg.QueryValueEx(key, app_name)
            return bool(val)
    except FileNotFoundError:
        return False
    except Exception:
        return False


def set_autostart_registry(enable=True):
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "GoogleCalendarHotkey"
    pythonw = sys.executable.replace("python.exe", "pythonw.exe")
    script_path = os.path.abspath(__file__)
    cmd = f'"{pythonw}" "{script_path}"'
    
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS) as key:
            if enable:
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, cmd)
            else:
                try:
                    winreg.DeleteValue(key, app_name)
                except FileNotFoundError:
                    pass
        return True
    except Exception as e:
        print(f"Error updating registry: {e}")
        return False


# ----------------- Main Application Class -----------------

class GoogleCalendarApp:
    def __init__(self):
        self.load_config()
        self.calendar_hwnd = None
        self.is_launching = False
        self.hwnd = None
        self.hicon = None
        self.nid = None
        self.wndproc_cb = WNDPROC(self.wnd_proc)
        
        # Single instance check via Mutex
        self.mutex = kernel32.CreateMutexW(None, False, "Global\\GoogleCalendarHotkey_SingleInstance")
        if kernel32.GetLastError() == 183: # ERROR_ALREADY_EXISTS
            print("Another instance of GoogleCalendarHotkey is already running.")
            self.toggle_calendar()
            sys.exit(0)

        # Autostart check
        if self.config.get("autostart", True):
            if not is_autostart_registered():
                set_autostart_registry(True)

        self.init_window()
        self.init_tray()
        self.register_hotkey()

        # Optional pre-load or open on boot
        if self.config.get("open_on_boot", False):
            self.toggle_calendar()
        elif self.config.get("preload_on_startup", False):
            threading.Thread(target=self._preload_hidden, daemon=True).start()

    def load_config(self):
        default_config = {
            "hotkey": "Ctrl+Alt+C",
            "browser": "auto",
            "autostart": True,
            "open_on_boot": False,
            "preload_on_startup": False,
            "use_custom_profile": False,
            "calendar_url": "https://calendar.google.com/calendar/r"
        }
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    self.config = {**default_config, **json.load(f)}
            except Exception:
                self.config = default_config
        else:
            self.config = default_config
            try:
                with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, indent=2, ensure_ascii=False)
            except Exception:
                pass

    def init_window(self):
        hinst = kernel32.GetModuleHandleW(None)
        class_name = "GoogleCalendarHotkeyClass"

        wc = WNDCLASSEXW()
        wc.cbSize = ctypes.sizeof(WNDCLASSEXW)
        wc.lpfnWndProc = self.wndproc_cb
        wc.hInstance = hinst
        wc.lpszClassName = class_name
        user32.RegisterClassExW(ctypes.byref(wc))

        self.hwnd = user32.CreateWindowExW(
            0, class_name, "GoogleCalendarHotkeyWindow",
            0, 0, 0, 0, 0,
            None, None, hinst, None
        )

    def init_tray(self):
        if os.path.exists(ICON_FILE):
            self.hicon = user32.LoadImageW(
                None, ICON_FILE, IMAGE_ICON, 16, 16, LR_LOADFROMFILE
            )
        if not self.hicon:
            self.hicon = user32.LoadIconW(0, 32512)

        tip = f"Google Calendar ({self.config.get('hotkey', 'Ctrl+Alt+C')})"
        self.nid = NOTIFYICONDATAW()
        self.nid.cbSize = ctypes.sizeof(NOTIFYICONDATAW)
        self.nid.hWnd = self.hwnd
        self.nid.uID = 1
        self.nid.uFlags = NIF_MESSAGE | NIF_ICON | NIF_TIP
        self.nid.uCallbackMessage = WM_TRAYICON
        self.nid.hIcon = self.hicon
        self.nid.szTip = tip[:127]

        shell32.Shell_NotifyIconW(NIM_ADD, ctypes.byref(self.nid))
        self.show_balloon("Google Calendar Hotkey", f"Sẵn sàng! Ấn {self.config.get('hotkey', 'Ctrl+Alt+C')} để Hiện/Ẩn Lịch.")

    def show_balloon(self, title, msg):
        if not self.nid:
            return
        b_nid = NOTIFYICONDATAW()
        b_nid.cbSize = ctypes.sizeof(NOTIFYICONDATAW)
        b_nid.hWnd = self.hwnd
        b_nid.uID = 1
        b_nid.uFlags = NIF_INFO
        b_nid.szInfoTitle = title[:63]
        b_nid.szInfo = msg[:255]
        b_nid.dwInfoFlags = NIIF_INFO
        shell32.Shell_NotifyIconW(NIM_MODIFY, ctypes.byref(b_nid))

    def register_hotkey(self):
        hotkey_str = self.config.get("hotkey", "Ctrl+Alt+C")
        try:
            mods, vk = parse_hotkey(hotkey_str)
            user32.UnregisterHotKey(self.hwnd, HOTKEY_ID)
            success = user32.RegisterHotKey(self.hwnd, HOTKEY_ID, mods, vk)
            if not success:
                self.show_balloon("Cảnh báo phím tắt", f"Không thể đăng ký {hotkey_str}. Phím có thể đang bị ứng dụng khác chiếm.")
        except Exception as e:
            self.show_balloon("Lỗi phím tắt", str(e))

    def find_calendar_window(self):
        found_hwnd = None
        
        def enum_proc(hwnd, lparam):
            nonlocal found_hwnd
            if not user32.IsWindow(hwnd):
                return True
            cls_buf = ctypes.create_unicode_buffer(256)
            user32.GetClassNameW(hwnd, cls_buf, 256)
            cls_name = cls_buf.value
            valid_classes = ("Chrome_WidgetWin_1", "Edge_WidgetWin_1", "MozillaWindowClass")
            if cls_name not in valid_classes:
                return True
                
            len_t = user32.GetWindowTextLengthW(hwnd)
            if len_t <= 0:
                return True
            title_buf = ctypes.create_unicode_buffer(len_t + 1)
            user32.GetWindowTextW(hwnd, title_buf, len_t + 1)
            title = title_buf.value.lower()
            
            # Filter out marketing landing page
            if "workspace.google.com" in title or "shareable online calendar" in title:
                return True
                
            keywords = ["google calendar", "lịch google", "google lịch", "google agenda", "calendar.google.com"]
            if any(k in title for k in keywords):
                is_tab = (" - google chrome" in title) or (" - microsoft edge" in title)
                if not is_tab:
                    found_hwnd = hwnd
                    return False
                elif found_hwnd is None:
                    found_hwnd = hwnd
            return True

        cb = WNDENUMPROC(enum_proc)
        user32.EnumWindows(cb, 0)
        return found_hwnd

    def force_foreground(self, hwnd):
        if not hwnd or not user32.IsWindow(hwnd):
            return
        user32.ShowWindow(hwnd, 9) # SW_RESTORE
        
        fore_hwnd = user32.GetForegroundWindow()
        fore_thread = user32.GetWindowThreadProcessId(fore_hwnd, None)
        app_thread = kernel32.GetCurrentThreadId()
        
        user32.keybd_event(0x12, 0, 0, 0)
        if fore_thread != app_thread:
            user32.AttachThreadInput(fore_thread, app_thread, True)
            user32.BringWindowToTop(hwnd)
            user32.SetForegroundWindow(hwnd)
            user32.AttachThreadInput(fore_thread, app_thread, False)
        else:
            user32.BringWindowToTop(hwnd)
            user32.SetForegroundWindow(hwnd)
        user32.keybd_event(0x12, 0, 2, 0)

    def _launch_worker(self):
        if self.is_launching:
            return
        self.is_launching = True
        try:
            pref = self.config.get("browser", "auto")
            browser_path, b_type = get_browser_executable(pref)

            if not browser_path:
                self.show_balloon("Lỗi", "Không tìm thấy Chrome hoặc Microsoft Edge trên máy tính!")
                return

            url = self.config.get("calendar_url", "https://calendar.google.com/calendar/r")
            
            if b_type == "firefox":
                args = [browser_path, "-new-window", url]
            else:
                args = [browser_path, f"--app={url}"]
            
            if self.config.get("use_custom_profile", False):
                profile_dir = os.path.join(os.getenv("LOCALAPPDATA", "."), "GoogleCalendarHotkey", "Profile")
                os.makedirs(profile_dir, exist_ok=True)
                args.append(f"--user-data-dir={profile_dir}")
                
            subprocess.Popen(args)

            for _ in range(50):
                time.sleep(0.1)
                hwnd = self.find_calendar_window()
                if hwnd:
                    self.calendar_hwnd = hwnd
                    self.force_foreground(hwnd)
                    break
        finally:
            self.is_launching = False

    def _preload_hidden(self):
        self._launch_worker()
        time.sleep(1.0)
        if self.calendar_hwnd and user32.IsWindow(self.calendar_hwnd):
            user32.ShowWindow(self.calendar_hwnd, 0) # SW_HIDE

    def toggle_calendar(self):
        if self.calendar_hwnd and user32.IsWindow(self.calendar_hwnd):
            is_visible = user32.IsWindowVisible(self.calendar_hwnd)
            is_min = user32.IsIconic(self.calendar_hwnd)
            fg_hwnd = user32.GetForegroundWindow()
            
            if is_visible and not is_min and (fg_hwnd == self.calendar_hwnd):
                user32.ShowWindow(self.calendar_hwnd, 0) # SW_HIDE
            else:
                user32.ShowWindow(self.calendar_hwnd, 5) # SW_SHOW
                user32.ShowWindow(self.calendar_hwnd, 9) # SW_RESTORE
                self.force_foreground(self.calendar_hwnd)
        else:
            hwnd = self.find_calendar_window()
            if hwnd:
                self.calendar_hwnd = hwnd
                user32.ShowWindow(hwnd, 5)
                user32.ShowWindow(hwnd, 9)
                self.force_foreground(hwnd)
            else:
                threading.Thread(target=self._launch_worker, daemon=True).start()

    def open_login_browser(self):
        pref = self.config.get("browser", "auto")
        browser_path, b_type = get_browser_executable(pref)
        login_url = "https://accounts.google.com/ServiceLogin?service=cl&continue=https%3A%2F%2Fcalendar.google.com%2Fcalendar%2Fr"
        if browser_path:
            subprocess.Popen([browser_path, login_url])
        else:
            os.startfile(login_url)
        self.show_balloon("Đăng nhập Google", "Hãy đăng nhập tài khoản trên trình duyệt vừa mở. Sau đó ấn Ctrl+Alt+C để dùng Lịch!")

    def show_context_menu(self):
        pt = POINT()
        user32.GetCursorPos(ctypes.byref(pt))

        hmenu = user32.CreatePopupMenu()
        user32.AppendMenuW(hmenu, MF_STRING, IDM_TOGGLE, f"📅 Hiện / Ẩn Lịch ({self.config.get('hotkey', 'Ctrl+Alt+C')})")
        user32.AppendMenuW(hmenu, MF_STRING, IDM_LOGIN, "🔑 Đăng nhập Google (Mở trình duyệt thường)")
        user32.AppendMenuW(hmenu, MF_SEPARATOR, 0, None)

        autostart_flag = MF_CHECKED if is_autostart_registered() else MF_UNCHECKED
        user32.AppendMenuW(hmenu, MF_STRING | autostart_flag, IDM_AUTOSTART, "🚀 Khởi động cùng Windows")
        user32.AppendMenuW(hmenu, MF_STRING, IDM_OPEN_CONFIG, "⚙️ Cài đặt (config.json)")
        user32.AppendMenuW(hmenu, MF_STRING, IDM_RELOAD, "🔄 Tải lại cấu hình")
        user32.AppendMenuW(hmenu, MF_SEPARATOR, 0, None)
        user32.AppendMenuW(hmenu, MF_STRING, IDM_EXIT, "❌ Thoát")

        user32.SetForegroundWindow(self.hwnd)
        cmd = user32.TrackPopupMenu(
            hmenu, TPM_RIGHTBUTTON | TPM_RETURNCMD,
            pt.x, pt.y, 0, self.hwnd, None
        )
        user32.PostMessageW(self.hwnd, 0, 0, 0)
        user32.DestroyMenu(hmenu)

        if cmd == IDM_TOGGLE:
            self.toggle_calendar()
        elif cmd == IDM_LOGIN:
            self.open_login_browser()
        elif cmd == IDM_AUTOSTART:
            current = is_autostart_registered()
            new_state = not current
            set_autostart_registry(new_state)
            self.config["autostart"] = new_state
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            status_text = "Đã BẬT" if new_state else "Đã TẮT"
            self.show_balloon("Khởi động cùng Windows", f"{status_text} tính năng tự động chạy khi mở máy.")
        elif cmd == IDM_OPEN_CONFIG:
            os.startfile(CONFIG_FILE)
        elif cmd == IDM_RELOAD:
            self.load_config()
            self.register_hotkey()
            tip = f"Google Calendar ({self.config.get('hotkey', 'Ctrl+Alt+C')})"
            self.nid.szTip = tip[:127]
            shell32.Shell_NotifyIconW(NIM_MODIFY, ctypes.byref(self.nid))
            self.show_balloon("Cập nhật", f"Đã áp dụng cấu hình mới! Phím tắt: {self.config.get('hotkey', 'Ctrl+Alt+C')}")
        elif cmd == IDM_EXIT:
            user32.DestroyWindow(self.hwnd)

    def wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == WM_HOTKEY:
            if wparam == HOTKEY_ID:
                self.toggle_calendar()
            return 0
        elif msg == WM_TRAYICON:
            if lparam == WM_LBUTTONUP:
                self.toggle_calendar()
            elif lparam == WM_RBUTTONUP:
                self.show_context_menu()
            return 0
        elif msg == WM_DESTROY:
            if self.nid:
                shell32.Shell_NotifyIconW(NIM_DELETE, ctypes.byref(self.nid))
            user32.UnregisterHotKey(hwnd, HOTKEY_ID)
            if self.hicon:
                user32.DestroyIcon(self.hicon)
            user32.PostQuitMessage(0)
            return 0
        return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

    def run(self):
        msg = wintypes.MSG()
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))


if __name__ == '__main__':
    app = GoogleCalendarApp()
    app.run()
