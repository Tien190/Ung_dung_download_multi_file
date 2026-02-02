(() => {
  let BASE_URL = "http://localhost:8000";
  // Các phần tử giao diện
  const urlList = document.getElementById("urlList");
  const addUrlBtn = document.getElementById("addUrl");
  const startAllBtn = document.getElementById("startAll");
  const msgArea = document.getElementById("msgArea");
  const tasksBody = document.getElementById("tasksBody");
  const localTasks = new Map();
  const deletedTaskIds = new Set();

  function showMsg(msg, type="error") {
    msgArea.innerHTML = `<b>${msg}</b>`;
    setTimeout(()=>msgArea.innerHTML="",3000);
  }

  function addUrlField(value = "") {
    const row = document.createElement("div");
    row.className = "row";
    const input = document.createElement("input");
    input.type = "text";
    input.placeholder = "Dán URL file trực tiếp (PDF, MP3, ZIP, PNG, JPG,...)";
    input.value = value;
    const remove = document.createElement("button");
    remove.textContent = "Xóa";
    remove.className = "danger";
    remove.onclick = () => urlList.removeChild(row);
    row.appendChild(input);
    row.appendChild(remove);
    urlList.appendChild(row);
  }
  addUrlBtn.addEventListener("click", () => addUrlField());
  addUrlField(); 
  addUrlField();

  async function downloadTaskFile(task_id, filename) {
    try {
      const url = `${BASE_URL}/api/file/${encodeURIComponent(task_id)}`;
      // Tạo thẻ a để browser thực hiện download file
      const link = document.createElement("a");
      link.href = url;
      link.download = filename;
      link.target = '_blank';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (err) { showMsg("Lỗi tải file: " + err);}
  }

  async function deleteTask(task_id) {
    if (!confirm("Xóa task này?")) return;
      deletedTaskIds.add(task_id);
      localTasks.delete(task_id);
      renderTasks(Object.fromEntries(localTasks));
    try {
      const res = await fetch(`${BASE_URL}/api/delete/${encodeURIComponent(task_id)}`, {
        method: "DELETE",
      });
      const data = await res.json();
      if (res.ok) {
        fetchTasks();
      } else {
        showMsg(data?.error || "Xóa thất bại!");
      }
    } catch (e) {
      showMsg("Lỗi xoá task: " + e);
    }
  }

  function renderTasks(tasksObjOrList) {
    let arr = [];
    if (Array.isArray(tasksObjOrList)) arr = tasksObjOrList;
    else if (tasksObjOrList && typeof tasksObjOrList === "object") {
      arr = Object.entries(tasksObjOrList).map(([task_id, t]) => ({ task_id, ...t }));
    }
    tasksBody.innerHTML = "";
    arr.forEach((t) => {
      if (deletedTaskIds.has(t.task_id)) return;
      localTasks.set(t.task_id, t);
      const tr = document.createElement("tr");
      const tdName = document.createElement("td");
      tdName.textContent = t.filename || "-";
      const tdStatus = document.createElement("td");
      tdStatus.textContent = (t.status || "").toLowerCase();
      tdStatus.className = "status " + (t.status||"");
      const tdProgress = document.createElement("td");
      const wrap = document.createElement("div");
      wrap.className = "progress-wrap";
      const bar = document.createElement("div");
      bar.className = "progress-bar";
      const pct = Number.isFinite(t.progress) && t.progress!==null ? t.progress : 0;
      bar.style.width = `${Math.max(0, Math.min(100, pct))}%`;
      wrap.appendChild(bar);
      tdProgress.appendChild(wrap);
      const tdSize = document.createElement("td");
      const total = t.total_size || 0;
      tdSize.textContent = total ? formatBytes(total) : "—";
      // Điều khiển: pause/resume/stop
      const tdCtrl = document.createElement("td");
      const pauseBtn = document.createElement("button");
      pauseBtn.textContent = "Pause";
      pauseBtn.onclick = () => pauseTask(t.task_id);
      pauseBtn.disabled = (t.status !== "downloading");
      const resumeBtn = document.createElement("button");
      resumeBtn.textContent = "Resume";
      resumeBtn.onclick = () => resumeTask(t.task_id);
      resumeBtn.disabled = (t.status !== "paused");
      const stopBtn = document.createElement("button");
      stopBtn.textContent = "Stop";
      stopBtn.className = "warn";
      stopBtn.onclick = () => stopTask(t.task_id);
      stopBtn.disabled = (t.status === "completed" || t.status === "stopped" || t.status === "error");
      tdCtrl.appendChild(pauseBtn);
      tdCtrl.appendChild(resumeBtn);
      tdCtrl.appendChild(stopBtn);
      // Nút tải file về máy nếu đã completed
      const tdDown = document.createElement("td");
      if (t.status==="completed") {
        const dBtn = document.createElement("button");
        dBtn.textContent = "Tải";
        dBtn.className = "ok";
        dBtn.onclick = ()=> downloadTaskFile(t.task_id, t.filename);
        tdDown.appendChild(dBtn);
      } else {
        tdDown.innerHTML = '<span class="muted"></span>';
      }
      // Nút XÓA task/cột XÓA, đặt ở cuối mỗi dòng
      const tdDelete = document.createElement("td");
      const delBtn = document.createElement("button");
      delBtn.textContent = "Xóa";
      delBtn.className = "danger";
      delBtn.onclick = () => deleteTask(t.task_id);
      tdDelete.appendChild(delBtn);
      // Thêm các ô vào dòng
      tr.appendChild(tdName);
      tr.appendChild(tdStatus);
      tr.appendChild(tdProgress);
      tr.appendChild(tdSize);
      tr.appendChild(tdCtrl);
      tr.appendChild(tdDown);
      tr.appendChild(tdDelete);  // Nút XÓA ở cuối
      tasksBody.appendChild(tr);
    });
  }

  function formatBytes(bytes) {
    const sizes = ["B", "KB", "MB", "GB", "TB"];
    if (!bytes || bytes === 0) return "0 B";
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    const val = (bytes / Math.pow(1024, i)).toFixed(2);
    return `${val} ${sizes[i]}`;
  }

  async function startDownloads() {
    const inputs = urlList.querySelectorAll('input[type="text"]');
    const urls = Array.from(inputs).map(i => i.value.trim()).filter(Boolean);
    if (!urls.length) return showMsg("Vui lòng nhập ít nhất một URL hợp lệ!");
    for (const url of urls) {
      try {
        console.log("Gọi API download:", `${BASE_URL}/api/download?url=${encodeURIComponent(url)}`);
        const res = await fetch(`${BASE_URL}/api/download?url=${encodeURIComponent(url)}`, { method: "POST" });
        if (!res.ok) throw new Error(await res.text());
        const data = await res.json();
        localTasks.set(data.task_id, {
          task_id: data.task_id, url,
          filename: url.split("/").pop() || "download.bin",
          status: "pending", progress: 0, total_size: 0
        });
      } catch (err) {
        showMsg(`Tạo task lỗi: ${err}`);
      }
    }
    renderTasks(Object.fromEntries([...localTasks.entries()]));
  }

  async function fetchTasks() {
    try {
      const res = await fetch(`${BASE_URL}/api/tasks`);
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      renderTasks(data);
    } catch {}
  }

  async function pauseTask(task_id) {
    try { 
      await fetch(`${BASE_URL}/api/pause/${encodeURIComponent(task_id)}`, { method: "POST" });
      fetchTasks();
    } catch (err) { showMsg("Pause thất bại: "+err);}
  }

  async function resumeTask(task_id) {
    try { 
      await fetch(`${BASE_URL}/api/resume/${encodeURIComponent(task_id)}`, { method: "POST" });
      fetchTasks();
    } catch (err) { showMsg("Resume thất bại: "+err);}
  }

  async function stopTask(task_id) {
    try { 
      await fetch(`${BASE_URL}/api/stop/${encodeURIComponent(task_id)}`, { method: "POST" });
      fetchTasks();
    } catch (err) { showMsg("Stop thất bại: "+err);}
  }

  // Polling 2s update tiến độ liên tục
  setInterval(fetchTasks, 2000);
  fetchTasks();
  startAllBtn.addEventListener("click", startDownloads);
})();