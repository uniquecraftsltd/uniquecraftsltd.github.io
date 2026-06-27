from pathlib import Path
import shutil

SOURCE = Path(
    "raw_photos/property_refurbishments/belsize-park-london"
)

DEST = Path(
    "img/projects/property_refurbishments"
)

print(f"Current directory: {Path.cwd()}")
print(f"SOURCE exists: {SOURCE.exists()}")
print(f"SOURCE path: {SOURCE.resolve()}")

DEST.mkdir(parents=True, exist_ok=True)

slug = SOURCE.name.lower().replace("_", "-").replace(" ", "-")

images = sorted([
    f for f in SOURCE.rglob("*")
    if f.is_file()
    and f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]
])

print(f"Found {len(images)} images")

for i, img in enumerate(images, start=1):
    ext = img.suffix.lower()

    new_name = f"{slug}-{i:03d}{ext}"

    shutil.copy2(
        img,
        DEST / new_name
    )

    print(f"✓ {img.relative_to(SOURCE)} → {new_name}")
