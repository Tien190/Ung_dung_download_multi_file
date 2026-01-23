import requests
import os
import time
from backend.src.models.download_task import DownloadStatus
from backend.config import CHUNK_SIZE

def download_file(task, folder):
    task.status = DownloadStatus.DOWNLOADING
    filepath = os.path.join(folder, task.filename)

    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36"),
        "Referer": "https://pixabay.com/",
    }

    try:
        with requests.get(task.url, headers=headers, stream=True, timeout=15) as r:
            r.raise_for_status()

            # 🔹 Lấy size file (có thể = 0 nếu server không cung cấp)
            total = r.headers.get("Content-Length")
            task.total_size = int(total) if total and total.isdigit() else 0

            downloaded = 0

            with open(filepath, "wb") as f:
                for chunk in r.iter_content(chunk_size=CHUNK_SIZE):

                    # ⏸ PAUSE mượt (đứng tại chỗ)
                    while task.status == DownloadStatus.PAUSED:
                        time.sleep(0.3)

                    # ⛔ STOP
                    if task.status == DownloadStatus.STOPPED:
                        f.close()
                        os.remove(filepath)
                        return

                    if not chunk:
                        continue

                    f.write(chunk)
                    downloaded += len(chunk)

                    # 🔥 CHỈ update progress khi có total_size
                    if task.total_size > 0:
                        task.progress = min(
                            int(downloaded * 100 / task.total_size), 100
                        )
                    else:
                        
                        task.progress = 0

        # chỉ completed khi không bị stop
        if task.status != DownloadStatus.STOPPED:
            task.progress = 100
            task.status = DownloadStatus.COMPLETED

    except Exception as e:
        print(">>> DOWNLOAD ERROR:", e)
        task.status = DownloadStatus.ERROR
