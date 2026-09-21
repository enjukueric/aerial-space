import os
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(ROOT, "img")

# (relative_path_in, relative_path_out, max_width)
MAX_W_DEFAULT = 1600
MAX_W_PORTRAIT = 900

total_before = 0
total_after = 0

for dirpath, dirnames, filenames in os.walk(IMG_DIR):
    for fn in filenames:
        if not fn.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        src = os.path.join(dirpath, fn)
        base, _ = os.path.splitext(fn)
        dst = os.path.join(dirpath, base + ".webp")

        before = os.path.getsize(src)
        total_before += before

        im = Image.open(src)
        if im.mode in ("RGBA", "P"):
            im = im.convert("RGBA")
        else:
            im = im.convert("RGB")

        max_w = MAX_W_PORTRAIT if "staff" in dirpath else MAX_W_DEFAULT
        if im.width > max_w:
            ratio = max_w / im.width
            im = im.resize((max_w, int(im.height * ratio)), Image.LANCZOS)

        im.save(dst, "WEBP", quality=82, method=6)
        after = os.path.getsize(dst)
        total_after += after
        print(f"{os.path.relpath(src, ROOT)}: {before/1024:.0f}KB -> {after/1024:.0f}KB")

        os.remove(src)

print(f"\nTOTAL: {total_before/1024/1024:.2f}MB -> {total_after/1024/1024:.2f}MB")
