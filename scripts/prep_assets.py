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
# Sources prefixed v9- come from PollenPal v9_Investors.pptx (2026-06-11).
# Unprefixed imageN names are the original 2026-04 deck extraction; entries
# whose deck source was dropped in v9 were removed here when the site images
# were replaced (device-grass, ml-algo, dashboard-phone).
IMAGE_MAP = [
    ("image24.jpeg",  "wendy-ventura.jpg", 1800),
    ("v9-deploy.jpeg", "device-deploy.jpg", 1200),
]

# (source gif, dest stem, crop "w:h:x:y" or None, crf)
# Output is <stem>.mp4 + <stem>-poster.jpg. Never upscaled.
# v9-detect-grid is cropped to the header + top two hive rows (B005, B003)
# so the panels survive the 240px-high cover crop in the step cards.
# v9-webapp-demo drops the nav sidebar; the fixed-height cover crop otherwise
# leaves a black sliver of it on the card's left edge.
VIDEO_MAP = [
    ("v9-detect-grid.gif", "ml-detect",   "984:604:0:0",  28),
    ("v9-webapp-demo.gif", "webapp-demo", "654:386:146:0", 30),
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


def encode_loop_video(src_gif: Path, dest_stem: str, crop: str | None, crf: int) -> None:
    dest_mp4 = DEST / f"{dest_stem}.mp4"
    dest_poster = DEST / f"{dest_stem}-poster.jpg"
    vf = (f"crop={crop}," if crop else "") + "scale=trunc(iw/2)*2:trunc(ih/2)*2"
    subprocess.run([
        FFMPEG, "-y", "-i", str(src_gif),
        "-movflags", "+faststart",
        "-pix_fmt", "yuv420p",
        "-vf", vf,
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", str(crf),
        "-an",
        str(dest_mp4),
    ], check=True)
    subprocess.run([
        FFMPEG, "-y", "-i", str(src_gif),
        "-frames:v", "1",
        "-update", "1",
        "-vf", vf,
        "-q:v", "3",
        str(dest_poster),
    ], check=True)
    print(f"  {dest_mp4.name:30s} {dest_mp4.stat().st_size // 1024} KB")
    print(f"  {dest_poster.name:30s} {dest_poster.stat().st_size // 1024} KB")


def main() -> None:
    DEST.mkdir(exist_ok=True)
    print(f"Using ffmpeg: {FFMPEG}")
    print("Optimizing images...")
    for src_name, dest_name, max_w in IMAGE_MAP:
        optimize_image(SRC / src_name, DEST / dest_name, max_w)
    print("Encoding hero video...")
    encode_hero_video(SRC / "image17.gif", DEST / "hero.mp4", DEST / "hero-poster.jpg")
    print("Encoding loop videos...")
    for src_name, dest_stem, crop, crf in VIDEO_MAP:
        encode_loop_video(SRC / src_name, dest_stem, crop, crf)
    print("Done.")


if __name__ == "__main__":
    main()
