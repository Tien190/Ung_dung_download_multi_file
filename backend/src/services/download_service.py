import os
import time
import requests
from backend.src.models.download_task import DownloadStatus


def download_file(task, download_folder, save_callback):
    filepath = os.path.join(download_folder, task.filename)

    try:
        headers = {}

        # Nếu file đã tồn tại → resume
        downloaded_size = 0
        if os.path.exists(filepath):
            downloaded_size = os.path.getsize(filepath)
            headers["Range"] = f"bytes={downloaded_size}-"

        task.status = DownloadStatus.DOWNLOADING

        with requests.get(task.url, stream=True, headers=headers, timeout=10) as r:
            r.raise_for_status()

            # Lấy tổng dung lượng file
            total_size = int(r.headers.get("content-length", 0))
            task.total_size = total_size + downloaded_size

            mode = "ab" if downloaded_size > 0 else "wb"

            with open(filepath, mode) as f:
                for chunk in r.iter_content(chunk_size=1024 * 512):  # 512KB
                    # 🛑 STOP
                    if task.status == DownloadStatus.STOPPED:
                        save_callback()
                        return

                    # ⏸ PAUSE
                    while task.status == DownloadStatus.PAUSED:
                        time.sleep(0.5)

                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)

                        # 📊 cập nhật tiến độ
                        if task.total_size > 0:
                            task.progress = int(downloaded_size * 100 / task.total_size)

                        save_callback()

        # ✅ HOÀN THÀNH
        task.progress = 100
        task.status = DownloadStatus.COMPLETED
        save_callback()

    except Exception as e:
        task.status = DownloadStatus.ERROR
        save_callback()
        print("Download error:", e)
