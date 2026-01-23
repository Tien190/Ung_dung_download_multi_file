# Multi File Download Manager – Backend

Backend cho ứng dụng **Multi File Download Manager**  
Xây dựng bằng **FastAPI**, hỗ trợ tải nhiều file, quản lý trạng thái download.


## 🚀 Công nghệ sử dụng
- Python 3.9+
- FastAPI
- Uvicorn
- Async / Background Task
- REST API

Chạy backend:
Cài thư viện: pip install -r backend/requirements.txt
Chạy: python -m uvicorn backend.main:app --reload

Mặc định sẽ ở http://localhost:8000
Chạy web-ui tĩnh:
Vào thư mục web-ui: cd web-ui
Chạy server tĩnh, ví dụ: python-m http.server5500
hoặc Node: npx serve .
Mở http://localhost:5500/public/index.html
Điền “Backend URL” là http://localhost:8000 rồi bấm “Dùng URL này”
Dán một vài URL và bấm “Bắt đầu tải tất cả”
Quan sát bảng “Tasks” và dùng nút Pause/Resume/Stop