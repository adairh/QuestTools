# QuestTools

QuestTools cung cấp cả giao diện web hiện đại lẫn bộ công cụ dòng lệnh để quản trị và trích xuất dữ liệu nhiệm vụ (quest)
cho các trò chơi nhập vai. Bộ công cụ đã được áp dụng cho tài liệu **“Cốt truyện và Nhiệm vụ Tân thủ”** và lưu trữ
thành cấu trúc JSON sẵn sàng sử dụng.

## Tính năng chính

- **Giao diện web chuyên nghiệp**: trình quản trị trực quan cho phép tìm kiếm, thêm, sửa, xoá nhiệm vụ, chỉnh sửa tổng quan
  tài liệu và xem ngay các đoạn hội thoại/ghi chú. Giao diện được xây dựng với Bootstrap 5, hỗ trợ bàn phím và cả thiết bị di động.
- **Đồng bộ trực tiếp với tập tin JSON**: mọi thao tác trong UI ghi nhận ngay vào tập tin dữ liệu, đảm bảo dữ liệu luôn nhất quán
  với các công cụ khác.
- **Bộ công cụ CLI đầy đủ**: tiếp tục hỗ trợ các lệnh `convert`, `list`, `show`, `add`, `update`, `remove` cho các quy trình tự động.
- **Bộ dữ liệu mẫu**: file `data/quests/tan_thu.json` đã được chuẩn hoá từ tài liệu gốc `data/raw/tan_thu.txt`.

## Cài đặt

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

## Giao diện quản trị web

Chạy máy chủ quản trị bằng lệnh:

```bash
python -m questtools serve data/quests/tan_thu.json --open
```

Trình duyệt sẽ mở đến `http://127.0.0.1:8000/` với các chức năng:

- Bảng điều hướng nhiệm vụ có tìm kiếm theo tiêu đề hoặc NPC.
- Biểu mẫu chỉnh sửa tổng quan tài liệu (tiêu đề, phần mô tả).
- Biểu mẫu chi tiết nhiệm vụ hỗ trợ các trường danh sách (mục tiêu, hội thoại, ghi chú) và trường mở rộng dạng JSON.
- Tạo nhiệm vụ mới, lưu thay đổi hoặc xoá ngay trên giao diện.

> Nếu muốn khởi động mà không tự mở trình duyệt, bỏ tuỳ chọn `--open`.

Bạn cũng có thể chạy launcher độc lập:

```bash
python -m questtools.ui_launcher --data data/quests/tan_thu.json --open
```

Launcher này là điểm vào được dùng cho bản đóng gói (PyInstaller).

## Bộ công cụ CLI truyền thống

Các lệnh CLI vẫn giữ nguyên. Ví dụ:

```bash
# Chuyển đổi tài liệu văn bản sang JSON
python -m questtools convert data/raw/tan_thu.txt data/quests/tan_thu.json --title "Cốt truyện và Nhiệm vụ Tân thủ"

# Liệt kê nhiệm vụ
python -m questtools list data/quests/tan_thu.json

# Xem chi tiết nhiệm vụ
python -m questtools show data/quests/tan_thu.json 3

# Thêm nhiệm vụ mới
python -m questtools add data/quests/tan_thu.json "Tên nhiệm vụ" --description "Mô tả" --targets "Điều kiện 1"

# Cập nhật hoặc xoá nhiệm vụ
python -m questtools update data/quests/tan_thu.json 3 --description "Mô tả mới"
python -m questtools remove data/quests/tan_thu.json 10
```

## Kiểm thử

Dự án sử dụng `unittest`:

```bash
python -m unittest discover
```

Các bài kiểm thử bao gồm cả lớp repository và API FastAPI.

## Đóng gói bản chạy độc lập

Bạn có thể dùng PyInstaller để tạo bản build chỉ cần tải về và chạy:

```bash
pip install pyinstaller
pyinstaller packaging/questtools_ui.spec
```

Sau khi hoàn tất, thư mục `dist/QuestToolsUI/` chứa file thực thi:

```bash
./dist/QuestToolsUI/QuestToolsUI --open
```

Tập tin JSON mẫu và các tài nguyên giao diện đã được gom sẵn trong bản build thông qua file spec.

## Thư mục dữ liệu

- `data/raw/tan_thu.txt` – tài liệu văn bản gốc.
- `data/quests/tan_thu.json` – kết quả chuyển đổi sang JSON.
