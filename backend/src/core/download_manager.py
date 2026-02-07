import os
import json
import threading
import uuid
from backend.src.models.download_task import DownloadTask, DownloadStatus
from backend.src.services.download_service import download_file
from backend.config import DOWNLOAD_FOLDER

TASK_FILE = "backend/src/storage/tasks.json"


class DownloadManager:
    def __init__(self):
        self.tasks = {}
        self.threads = {}
        os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
        os.makedirs(os.path.dirname(TASK_FILE), exist_ok=True)
        self.load_tasks()

    # ================= SAVE / LOAD =================

    def save_tasks(self):
        data = {
            tid: {
                "task_id": t.task_id,
                "url": t.url,
                "filename": t.filename,
                "status": t.status,
                "progress": t.progress,
                "total_size": t.total_size
            } for tid, t in self.tasks.items()
        }
        with open(TASK_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def load_tasks(self):
        if not os.path.exists(TASK_FILE):
            return

        with open(TASK_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        for tid, info in data.items():
            task = DownloadTask(tid, info["url"], info["filename"])
            task.status = info["status"]
            task.progress = info["progress"]
            task.total_size = info["total_size"]

            filepath = os.path.join(DOWNLOAD_FOLDER, task.filename)

            if os.path.exists(filepath) and task.total_size > 0:
                downloaded_size = os.path.getsize(filepath)
                task.progress = int(downloaded_size * 100 / task.total_size)

            # Nếu đang tải dở trước khi tắt server → cho pause
            if task.status == DownloadStatus.DOWNLOADING:
                task.status = DownloadStatus.PAUSED

            self.tasks[tid] = task

    # ================= THREAD START =================

    def start_thread(self, task):
        thread = threading.Thread(
            target=download_file,
            args=(task, DOWNLOAD_FOLDER, self.save_tasks),
            daemon=True
        )
        self.threads[task.task_id] = thread
        thread.start()

    # ================= TASK HANDLING =================

    def create_task(self, url: str):
        task_id = str(uuid.uuid4())
        filename = url.split("/")[-1]
        task = DownloadTask(task_id, url, filename)
        self.tasks[task_id] = task
        self.save_tasks()
        self.start_thread(task)
        return task

    def pause(self, task_id):
        task = self.tasks[task_id]
        task.status = DownloadStatus.PAUSED
        self.save_tasks()

    def resume(self, task_id):
        task = self.tasks[task_id]

        # 🔥 CHỈ resume nếu không có thread đang chạy
        if task_id in self.threads and self.threads[task_id].is_alive():
            task.status = DownloadStatus.DOWNLOADING
            return

        task.status = DownloadStatus.DOWNLOADING
        self.save_tasks()
        self.start_thread(task)

    def stop(self, task_id):
        task = self.tasks[task_id]
        task.status = DownloadStatus.STOPPED
        self.save_tasks()

    def get_all(self):
        return self.tasks


download_manager = DownloadManager()
