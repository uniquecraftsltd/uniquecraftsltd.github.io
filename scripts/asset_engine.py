import sqlite3
import shutil
import json
import argparse
import logging
from pathlib import Path
from typing import Final

BASE_DIR: Final = Path(__file__).resolve().parents[1]
RAW_ROOT: Final = BASE_DIR / "raw_photos"
DEST_ROOT: Final = BASE_DIR / "img/projects"
DB_PATH: Final = BASE_DIR / "sape_core.db"
MANIFEST_PATH: Final = DEST_ROOT / "global_manifest.json"

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class AssetEngine:
    def __init__(self):
        self.db = sqlite3.connect(DB_PATH)
        self._init_db()

    def _init_db(self):
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS assets (logical_id TEXT PRIMARY KEY, dst_path TEXT, project TEXT);
        """)

    def sync(self, target_project=None):
        # اگر پروژه خاصی مد نظر نیست، دیتابیس را کاملا پاک می‌کنیم
        if not target_project:
            self.db.execute("DELETE FROM assets")
        else:
            # اگر فقط یک پروژه است، فقط همان را پاک می‌کنیم
            self.db.execute("DELETE FROM assets WHERE project = ?", (target_project,))

        for project_dir in RAW_ROOT.rglob("*"):
            if project_dir.is_dir():
                if target_project and project_dir.name != target_project:
                    continue

                images = sorted([f for f in project_dir.iterdir() if f.suffix.lower() in {".jpg", ".png", ".webp"}])

                for i, src in enumerate(images, start=1):
                    new_name = f"{project_dir.name.lower().replace('_', '-')}-{i:03d}{src.suffix.lower()}"
                    dst_folder = DEST_ROOT / project_dir.name
                    dst_folder.mkdir(parents=True, exist_ok=True)
                    dst = dst_folder / new_name

                    shutil.copy2(src, dst)
                    self.db.execute("INSERT OR REPLACE INTO assets VALUES (?, ?, ?)",
                                    (new_name, str(dst), project_dir.name))
                    logging.info(f"Synced: {project_dir.name} -> {new_name}")

        self.db.commit()
        self.generate_manifest()

    def generate_manifest(self):
        projects = self.db.execute("SELECT DISTINCT project FROM assets").fetchall()
        manifest = []

        for (project_name,) in projects:
            # پیدا کردن دارایی‌ها (عکس‌ها)
            assets = self.db.execute("SELECT logical_id FROM assets WHERE project = ?", (project_name,)).fetchall()

            # خواندن توضیحات از فایل متنی (اگر وجود داشت)
            desc_path = RAW_ROOT / project_name / "description.txt"
            description = ""
            if desc_path.exists():
                description = desc_path.read_text(encoding="utf-8").strip()

            manifest.append({
                "id": project_name.lower().replace("_", "-"),
                "title": project_name.replace("_", " ").title(),
                "description": description, # اضافه شدن این فیلد
                "gallery": sorted([f"img/projects/{project_name}/{a[0]}" for a in assets])
            })

        with open(MANIFEST_PATH, "w") as f:
            json.dump(manifest, f, indent=2)
            
    def run_cli(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="cmd")
        sync_parser = subparsers.add_parser("sync")
        sync_parser.add_argument("--project", help="Specific project to sync")

        args = parser.parse_args()
        if args.cmd == "sync":
            self.sync(args.project)

if __name__ == "__main__":
    AssetEngine().run_cli()
