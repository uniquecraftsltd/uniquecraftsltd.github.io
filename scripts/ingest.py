import shutil
from pathlib import Path

# تنظیم مسیرها
# توجه: دقت کنید که نام کاربری parvizmossiyeri دقیقاً همین است
NEX_SPACE = Path("/Users/parvizmossiyeri/Desktop/Nex_space")
RAW_PHOTOS = Path(__file__).resolve().parents[1] / "raw_photos"

def ingest():
    print(f"Checking NEX_SPACE: {NEX_SPACE.exists()}")
    if not NEX_SPACE.exists():
        print("Error: Nex_space folder not found on Desktop!")
        return

    count = 0
    for src_file in NEX_SPACE.rglob("*"):
        if src_file.is_file() and src_file.suffix.lower() in {".jpg", ".png", ".webp", ".jpeg"}:
            # محاسبه مسیر نسبی برای حفظ ساختار پوشه‌ها
            rel_path = src_file.relative_to(NEX_SPACE)
            dst_file = RAW_PHOTOS / rel_path

            if not dst_file.exists():
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dst_file)
                print(f"✓ Copied: {rel_path}")
                count += 1
            else:
                # اگر فایل قبلاً وجود دارد، نادیده می‌گیرد
                pass

    print(f"Ingestion finished. {count} new files copied.")

if __name__ == "__main__":
    ingest()
