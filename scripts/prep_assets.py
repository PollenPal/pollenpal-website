"""One-shot script: optimize deck media for the website.

Reads pre-extracted deck images from .superpowers/deck_media/, optimizes them
for web, and writes them into images/ with semantic filenames. Also re-encodes
the 360-apiary GIF into a small MP4 + JPEG poster for the hero.
"""
import subprocess
from pathlib import Path
from PIL import Image
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / ".superpowers" / "deck_media"
DEST = ROOT / "images"

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

# (source filename, dest filename, max width)
IMAGE_MAP = [
    ("image5.png",   "device-grass.jpg",        1400),
    ("image32.png",  "ml-detection.jpg",        1400),
    ("image6.png",   "dashboard-phone.jpg",     1200),
    ("image24.jpeg", "wendy-ventura.jpg",       1800),
    ("image35.png",  "device-field.jpg",        1600),
    ("image34.png",  "device-cad.jpg",          1200),
    ("image7.png",   "ml-detection-simple.jpg", 1400),
    ("image25.jpeg", "nyc-rooftop.jpg",         1600),
]


def optimize_image(src: Path, dest: Path, max_width: int) -> None:
    im = Image.open(src).convert("RGB")
    if im.width > max_width:
        ratio = max_width / im.width
        im = im.resize((max_width, int(im.height * ratio)), Image.LANCZOS)
    im.save(dest, "JPEG", quality=82, optimize=True, progressive=True)
    print(f"  {dest.name:30s} {dest.stat().st_size // 1024} KB")


def encode_hero_video(src_gif: Path, dest_mp4: Path, dest_poster: Path) -> None:
    # Source GIF is 190x336. Cap output at ~380w (2x source) so we don't waste
    # bits upscaling. CSS scales the video into a 440px frame on screen.
    subprocess.run([
        FFMPEG, "-y", "-i", str(src_gif),
        "-movflags", "+faststart",
        "-pix_fmt", "yuv420p",
        "-vf", "scale='min(380,iw*2)':-2:flags=lanczos",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "28",
        "-an",
        str(dest_mp4),
    ], check=True)
    subprocess.run([
        FFMPEG, "-y", "-i", str(src_gif),
        "-frames:v", "1",
        "-update", "1",
        "-vf", "scale='min(380,iw*2)':-2:flags=lanczos",
        "-q:v", "3",
        str(dest_poster),
    ], check=True)
    print(f"  hero.mp4         {dest_mp4.stat().st_size // 1024} KB")
    print(f"  hero-poster.jpg  {dest_poster.stat().st_size // 1024} KB")


def main() -> None:
    DEST.mkdir(exist_ok=True)
    print(f"Using ffmpeg: {FFMPEG}")
    print("Optimizing images...")
    for src_name, dest_name, max_w in IMAGE_MAP:
        optimize_image(SRC / src_name, DEST / dest_name, max_w)
    print("Encoding hero video...")
    encode_hero_video(SRC / "image17.gif", DEST / "hero.mp4", DEST / "hero-poster.jpg")
    print("Done.")


if __name__ == "__main__":
    main()
