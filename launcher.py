import customtkinter as ctk
import requests
import zipfile
import os
import subprocess
import json
import threading
import sys
import shutil

class Launcher(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Trình Khởi Chạy - Hệ Thống POS")
        self.geometry("450x180")
        self.eval('tk::PlaceWindow . center')
        self.resizable(False, False)
        
        self.status_label = ctk.CTkLabel(self, text="Đang kiểm tra phiên bản mới...", font=("Arial", 16))
        self.status_label.pack(pady=(30, 10))
        
        self.progress_bar = ctk.CTkProgressBar(self, width=350, height=15)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)
        
        self.remote_url = "https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/YOUR_REPO/main/version.json"
        self.local_version_file = "version.json"
        self.main_exe = "app.exe"
        
        self.after(500, self.start_worker)

    def start_worker(self):
        threading.Thread(target=self.run_update_logic, daemon=True).start()

    def run_update_logic(self):
        try:
            local_version = "0.0.0"
            if os.path.exists(self.local_version_file):
                with open(self.local_version_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    local_version = data.get("version", "0.0.0")

            response = requests.get(self.remote_url, timeout=5)
            if response.status_code == 200:
                remote_data = response.json()
                remote_version = remote_data.get("version", "0.0.0")
                download_url = remote_data.get("url", "")

                if self.is_newer(remote_version, local_version):
                    self.status_label.configure(text=f"Đang tải bản cập nhật {remote_version}...")
                    success = self.download_and_extract(download_url)
                    if success:
                        with open(self.local_version_file, "w", encoding="utf-8") as f:
                            json.dump({"version": remote_version}, f)
                else:
                    self.status_label.configure(text="Phiên bản đã cập nhật nhất!")
        except:
            self.status_label.configure(text="Không thể kết nối máy chủ, mở bản offline...")

        self.after(1000, self.launch_main_app)

    def is_newer(self, remote, local):
        r_parts = [int(x) for x in remote.split(".")]
        l_parts = [int(x) for x in local.split(".")]
        for r, l in zip(r_parts, l_parts):
            if r > l: return True
            elif r < l: return False
        return False

    def download_and_extract(self, url):
        zip_path = "update_temp.zip"
        try:
            response = requests.get(url, stream=True, timeout=10)
            total_size = int(response.headers.get('content-length', 0))
            wrote = 0
            
            with open(zip_path, 'wb') as file:
                for data in response.iter_content(1024):
                    wrote += len(data)
                    file.write(data)
                    if total_size > 0:
                        self.progress_bar.set(wrote / total_size)

            self.status_label.configure(text="Đang giải nén và cài đặt...")
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall("temp_extracted")

            for root, dirs, files in os.walk("temp_extracted"):
                for file in files:
                    src_file = os.path.join(root, file)
                    rel_path = os.path.relpath(src_file, "temp_extracted")
                    dest_file = os.path.join(os.getcwd(), rel_path)
                    
                    os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                    if dest_file != os.path.abspath(sys.argv[0]): 
                        shutil.copy2(src_file, dest_file)

            shutil.rmtree("temp_extracted")
            os.remove(zip_path)
            return True
        except:
            if os.path.exists(zip_path): os.remove(zip_path)
            if os.path.exists("temp_extracted"): shutil.rmtree("temp_extracted")
            return False

    def launch_main_app(self):
        if os.path.exists(self.main_exe):
            subprocess.Popen([self.main_exe])
        self.quit()

if __name__ == "__main__":
    app = Launcher()
    app.mainloop()