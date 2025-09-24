# QuestTools

QuestTools cung cấp bộ công cụ dòng lệnh để quản trị và trích xuất dữ liệu nhiệm vụ (quest) từ các tài liệu dạng văn bản thô.
Bộ công cụ đã được sử dụng để chuyển đổi tài liệu **“Cốt truyện và Nhiệm vụ Tân thủ”** thành dữ liệu JSON có cấu trúc và đi kèm
các lệnh hỗ trợ quản lý, cập nhật dữ liệu.

## Các tính năng chính

* Chuyển đổi tài liệu văn bản định dạng danh sách nhiệm vụ sang JSON.
* Liệt kê, hiển thị chi tiết từng nhiệm vụ từ tập tin JSON.
* Thêm, cập nhật, xóa nhiệm vụ trực tiếp thông qua dòng lệnh.
* Mẫu dữ liệu thực tế của bộ nhiệm vụ Tân thủ (`data/quests/tan_thu.json`).

## Sử dụng nhanh

Các ví dụ dưới đây giả định bạn đang đứng tại thư mục gốc của dự án.

```bash
# Chuyển đổi tài liệu văn bản sang JSON
python -m questtools convert data/raw/tan_thu.txt data/quests/tan_thu.json --title "Cốt truyện và Nhiệm vụ Tân thủ"

# Liệt kê các nhiệm vụ
python -m questtools list data/quests/tan_thu.json

# Xem chi tiết nhiệm vụ có id = 3
python -m questtools show data/quests/tan_thu.json 3

# Thêm nhiệm vụ mới
python -m questtools add data/quests/tan_thu.json "Tên nhiệm vụ" \
    --description "Mô tả nhiệm vụ" \
    --accept-npc "NPC nhận" \
    --targets "Hoàn thành điều kiện 1" --targets "Hoàn thành điều kiện 2"

# Cập nhật nhiệm vụ hiện có
python -m questtools update data/quests/tan_thu.json 3 --description "Mô tả mới"

# Xóa nhiệm vụ khỏi danh sách
python -m questtools remove data/quests/tan_thu.json 10
```

Các lệnh `add` và `update` hỗ trợ các tham số lặp (`--dialog-accept`, `--dialog-complete`, `--targets`, `--notes`) để khai báo
nhiều dòng hội thoại hoặc mục tiêu.

## Cấu trúc dữ liệu

Tập tin JSON được tạo ra có dạng:

```json
{
  "title": "Cốt truyện và Nhiệm vụ Tân thủ",
  "overview": "...",
  "quests": [
    {
      "id": 1,
      "title": "Rừng tre ban sớm",
      "description": "...",
      "accept_npc": "...",
      "dialog_accept": ["..."],
      "targets": ["..."],
      "notes": ["..."],
      "extra_fields": {}
    }
  ]
}
```

## Chạy kiểm thử

Dự án sử dụng `unittest` cho bộ kiểm thử đơn giản:

```bash
python -m unittest
```

## Thư mục dữ liệu

* `data/raw/tan_thu.txt` – tài liệu văn bản gốc.
* `data/quests/tan_thu.json` – kết quả chuyển đổi sang JSON.

## Phát triển thêm

Bộ công cụ được xây dựng bằng Python thuần, không phụ thuộc vào thư viện ngoài. Bạn có thể mở rộng bằng cách bổ sung các lệnh mới
hoặc tinh chỉnh bộ phân tích trong `questtools/parser.py` để phù hợp với định dạng tài liệu của riêng mình.
