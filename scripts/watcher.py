import time, subprocess, os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    # متغیر برای جلوگیری از اجرای تکراری
    last_run = 0

    def on_created(self, event):
        # جلوگیری از اجرای سریع پشت سر هم (Debounce 5 seconds)
        if time.time() - self.last_run < 5:
            return

        if not event.is_directory and event.src_path.lower().endswith(('.jpg', '.png', '.webp', '.jpeg')):
            # استخراج نام پوشه والد (پروژه)
            project_name = os.path.basename(os.path.dirname(event.src_path))

            # اگر فایل در ریشه اصلی بود و پروژه نداشت، نامش را Nex_space بگذار
            if project_name == "Nex_space": return

            print(f"\n[ACTION] Detected change in: '{project_name}'. Syncing...")

            # ثبت زمان اجرا برای جلوگیری از تکرار
            self.last_run = time.time()

            # اجرای مراحل
            subprocess.run(["python3", "scripts/ingest.py"])
            subprocess.run(["python3", "scripts/asset_engine.py", "sync", "--project", project_name])

            print(f"[SUCCESS] Sync for '{project_name}' finished.")

if __name__ == "__main__":
    observer = Observer()
    # نظارت بر مسیر
    observer.schedule(ChangeHandler(), "/Users/parvizmossiyeri/Desktop/Nex_space", recursive=True)
    observer.start()
    print("Watcher is running... Press Ctrl+C to stop.")
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt: observer.stop()
    observer.join()
