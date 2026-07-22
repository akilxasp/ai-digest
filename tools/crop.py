"""Fetch an image, centre-crop it to 21:9, and save it into assets/.

Usage:  python3 tools/crop.py <image-url> <slug>
Prints the raw.githubusercontent URL to put in the template.

Raw URLs are used rather than the Pages URL because Pages takes a minute to
redeploy after a push, and the digest email goes out immediately.
"""
import io
import pathlib
import subprocess
import sys
import urllib.request

RATIO = 21 / 9
WIDTH = 1400
REPO = "akilxasp/ai-digest"
UA = "ai-digest/1.0 (https://github.com/akilxasp/ai-digest)"

try:
    from PIL import Image
except ModuleNotFoundError:
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "Pillow"], check=True)
    from PIL import Image


def main(url: str, slug: str) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        img = Image.open(io.BytesIO(r.read()))

    img = img.convert("RGB")
    w, h = img.size

    # centre-crop to 21:9, taking the limiting dimension
    if w / h > RATIO:
        new_w = int(h * RATIO)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / RATIO)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))

    img = img.resize((WIDTH, int(WIDTH / RATIO)), Image.LANCZOS)

    out = pathlib.Path("assets") / f"{slug}.jpg"
    out.parent.mkdir(exist_ok=True)
    img.save(out, "JPEG", quality=82, optimize=True)

    print(f"https://raw.githubusercontent.com/{REPO}/main/{out.as_posix()}")
    print(f"  {out} — {out.stat().st_size // 1024}KB", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: python3 tools/crop.py <image-url> <slug>")
    main(sys.argv[1], sys.argv[2])
