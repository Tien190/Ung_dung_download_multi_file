# 🌦️ Trạm Thời Tiết Đa Nguồn (Multi-Source Weather Station)

Đây là một dự án ứng dụng xem thời tiết trên desktop, được xây dựng với kiến trúc Client-Server, sử dụng lập trình bất đồng bộ để mang lại trải nghiệm mượt mà và real-time.

## ✨ Tính năng (Dự kiến)

- [ ] **Giao diện người dùng (GUI)** trực quan và thân thiện.
- [ ] **Tìm kiếm thành phố thông minh:** Tự động gợi ý thành phố khi người dùng gõ.
- [ ] **Tích hợp đa nguồn API:**
    - [ ] Lấy thông tin thời tiết chính (nhiệt độ, độ ẩm, gió...).
    - [ ] Lấy chỉ số chất lượng không khí (AQI).
    - [ ] Hiển thị hình ảnh của thành phố làm nền.
- [ ] **Biểu đồ trực quan:** Vẽ biểu đồ dự báo nhiệt độ trong 24 giờ tới.
- [ ] **Tự động cập nhật:** Dữ liệu thời tiết tự làm mới sau mỗi 30 phút.
- [ ] **Giao tiếp Client-Server:** Sử dụng `socket` và `asyncio` để truyền dữ liệu.

## 🛠️ Công nghệ sử dụng

*   **Ngôn ngữ:** Python 3
*   **Lập trình bất đồng bộ:** `asyncio`
*   **Giao diện (Frontend):** `Tkinter` (hoặc `PyQt6`/`PySide6`)
*   **Giao tiếp mạng:** `socket`
*   **Yêu cầu HTTP (cho API):** `aiohttp`

## 📂 Cấu trúc dự án

```
/
|-- backend/     # Toàn bộ code của Server
|-- frontend/    # Toàn bộ code của Client (GUI)
|-- docs/        # Tài liệu thiết kế
`-- .gitignore, README.md
```

- **`backend/`**: Chịu trách nhiệm lắng nghe kết nối từ client, xử lý logic nghiệp vụ, gọi đến các API thời tiết bên ngoài và gửi dữ liệu về cho client.
- **`frontend/`**: Chịu trách nhiệm hiển thị giao diện người dùng, gửi yêu cầu lên server và lắng nghe, cập nhật dữ liệu từ server.

## 🚀 Bắt đầu

### Yêu cầu

*   Python 3.8+

### Cài đặt và Chạy Backend

1.  Di chuyển vào thư mục backend:
    ```bash
    cd backend
    ```
2.  Tạo và kích hoạt môi trường ảo:
    ```bash
    # Trên Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Trên macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Cài đặt các thư viện cần thiết:
    ```bash
    pip install -r requirements.txt
    ```
4.  Chạy server:
    ```bash
    python src/main.py
    ```
    Server sẽ bắt đầu lắng nghe trên `127.0.0.1:8888`.

### Cài đặt và Chạy Frontend

1.  Mở một terminal mới, di chuyển vào thư mục frontend:
    ```bash
    cd frontend
    ```
2.  (Tùy chọn nhưng khuyến khích) Tạo và kích hoạt môi trường ảo riêng:
    ```bash
    # Trên Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Trên macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Cài đặt các thư viện cần thiết:
    ```bash
    pip install -r requirements.txt
    ```
4.  Chạy ứng dụng client:
    ```bash
    python src/main.py
    ```

# Weather Backend API

## Run
pip install -r requirements.txt
uvicorn main:app --reload

## Endpoints
GET /weather?city=Hanoi
GET /forecast?city=Hanoi
GET /cities?q=Ha
---
*Dự án được tạo ra với mục đích học tập và thực hành lập trình bất đồng bộ trong Python.*