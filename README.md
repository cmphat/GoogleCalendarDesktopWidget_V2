# 📅 Google Calendar Hotkey & Autostart cho Windows

Tiện ích nhẹ nhàng, chạy ngầm trên Windows giúp bạn **gọi và ẩn Google Calendar chỉ bằng 1 tổ hợp phím tắt**, đồng thời **tự động khởi động cùng Windows**.

---

## ✨ Tính năng nổi bật

- ⚡ **Hiện / Ẩn tức thì**: Nhấn phím tắt (`Ctrl + Alt + C` mặc định) để mở hoặc đưa Calendar lên đầu. Nhấn lần nữa khi đang dùng sẽ tự động ẩn đi.
- 🚀 **Tự khởi động cùng Windows**: Tự động chạy ngầm mỗi khi mở máy (không hiện cửa sổ cmd đen gây khó chịu).
- 🎨 **Giao diện App độc lập (PWA)**: Mở Google Calendar dưới dạng ứng dụng độc lập, không viền, không thanh URL, sạch sẽ và mượt mà.
- 🔑 **Giữ nguyên đăng nhập**: Sử dụng profile trình duyệt Chrome hoặc Edge hiện tại của bạn, không cần đăng nhập lại tài khoản Google.
- 📌 **Khay hệ thống (System Tray)**: Biểu tượng lịch nhỏ gọn ở góc dưới bên phải màn hình (cạnh đồng hồ) với menu chuột phải tiện lợi.
- ⚙️ **Dễ dàng đổi phím tắt**: Tùy chỉnh bất kỳ phím nào bạn thích (`Ctrl+Alt+C`, `Alt+C`, `F12`, `Win+Alt+C`, v.v.) qua file `config.json`.

---

## 🚀 Cách cài đặt & Sử dụng (Chỉ 1 Click)

1. Mở thư mục:
   ```
   C:\Users\ADMIN\.gemini\antigravity\scratch\google_calendar_hotkey
   ```
2. Nhấp đúp vào file **`install_autostart.bat`**.
3. Xong! Ứng dụng sẽ tự động được thêm vào khởi động Windows và chạy ngầm ngay lập tức.
4. Thử ấn **`Ctrl + Alt + C`** để trải nghiệm!

---

## ⌨️ Cách đổi phím tắt khác

Mở file **`config.json`** trong thư mục (hoặc nhấp chuột phải vào icon khay hệ thống chọn **⚙️ Cài đặt (config.json)**):

```json
{
  "hotkey": "Ctrl+Alt+C",
  "browser": "auto",
  "autostart": true,
  "open_on_boot": false,
  "use_custom_profile": false,
  "calendar_url": "https://calendar.google.com"
}
```

Một số gợi ý phím tắt bạn có thể đổi:
- `"Alt+C"`: Tiện lợi và nhanh gọn
- `"Ctrl+Shift+C"`: Dễ bấm một tay
- `"F12"`: Một phím duy nhất
- `"Win+Alt+C"`: Tránh trùng với các ứng dụng khác

Sau khi sửa `config.json`, nhấp chuột phải vào biểu tượng lịch ở khay hệ thống và chọn **🔄 Tải lại cấu hình** (hoặc chạy lại `start.bat`).

---

## 🛑 Cách gỡ bỏ hoặc tạm dừng

- **Tạm dừng**: Nhấp chuột phải vào icon ở khay hệ thống chọn **❌ Thoát** (hoặc chạy file `stop.bat`).
- **Gỡ bỏ tự khởi động hoàn toàn**: Nhấp đúp vào file **`uninstall_autostart.bat`**.
