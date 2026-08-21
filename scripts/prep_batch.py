#!/usr/bin/env python3
r"""
prep_batch.py — process a batch of newly scanned/cropped illustrations:

  1. Rename each image into the archive's naming convention (Latin/ASCII,
     auto-transliterated from Georgian input where needed).
  2. Generate web-optimized derivatives (full size + thumbnail, JPEG + WebP).
  3. Write a front-matter stub file per image into _illustrations/, with
     everything pre-filled except caption, theme_tags, and artist.

Windows-compatible: uses pathlib throughout, and explicitly opens every text
file as UTF-8 (Windows' default text encoding is NOT UTF-8, which silently
corrupts Georgian text if left unspecified).

Usage (PowerShell):
    python scripts\prep_batch.py `
        --journal droeba `
        --date 1883-04-12 `
        --issue no042 `
        --theme "ომი" `
        illustrations-source\new-batch\

If a batch spans more than one theme, run this once per theme (or per
subfolder) rather than trying to handle multiple themes in one call.

Requires: pip install pillow pyyaml
"""
import argparse
import shutil
import sys
from datetime import date as dt
from pathlib import Path

import yaml
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent
JOURNALS_FILE = REPO_ROOT / "data" / "journals.yml"
ILLUSTRATIONS_DIR = REPO_ROOT / "_illustrations"
IMAGES_FULL_DIR = REPO_ROOT / "assets" / "images" / "illustrations" / "full"
IMAGES_THUMB_DIR = REPO_ROOT / "assets" / "images" / "illustrations" / "thumb"

FULL_MAX_EDGE = 1800
THUMB_WIDTH = 480
FULL_QUALITY = 82
THUMB_QUALITY = 78

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}

# Georgian -> Latin, National System (2002): the same romanization used on
# Georgian road signs, driving licences, and by Google Maps/Translate,
# adopted by BGN/PCGN in 2009. Fixed and deterministic, so slugs stay
# predictable even though some letter pairs collide (e.g. კ/ქ both -> k) —
# that's a known, accepted property of this system, not a bug here.
GEORGIAN_TO_LATIN = {
    "ა": "a", "ბ": "b", "გ": "g", "დ": "d", "ე": "e", "ვ": "v", "ზ": "z",
    "თ": "t", "ი": "i", "კ": "k", "ლ": "l", "მ": "m", "ნ": "n", "ო": "o",
    "პ": "p", "ჟ": "zh", "რ": "r", "ს": "s", "ტ": "t", "უ": "u", "ფ": "p",
    "ქ": "k", "ღ": "gh", "ყ": "q", "შ": "sh", "ჩ": "ch", "ც": "ts",
    "ძ": "dz", "წ": "ts", "ჭ": "ch", "ხ": "kh", "ჯ": "j", "ჰ": "h",
}


def transliterate(text: str) -> str:
    """Convert Georgian text to a Latin slug fragment. Passes through any
    characters that are already Latin/ASCII (so mixed input is safe too)."""
    return "".join(GEORGIAN_TO_LATIN.get(ch, ch) for ch in text)


def slugify(text: str) -> str:
    latin = transliterate(text.strip().lower())
    return "-".join(latin.split())


def load_journals() -> dict:
    if not JOURNALS_FILE.exists():
        sys.exit(f"Missing {JOURNALS_FILE}. Add your journal slugs there first.")
    return yaml.safe_load(JOURNALS_FILE.read_text(encoding="utf-8")) or {}


def process_image(src_path: Path, dest_stem: str) -> tuple[int, int]:
    """Generate full + thumbnail derivatives, return original (width, height)."""
    IMAGES_FULL_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_THUMB_DIR.mkdir(parents=True, exist_ok=True)

    with Image.open(src_path) as img:
        img = img.convert("RGB")
        width, height = img.size

        full = img.copy()
        full.thumbnail((FULL_MAX_EDGE, FULL_MAX_EDGE))
        full.save(IMAGES_FULL_DIR / f"{dest_stem}.jpg", "JPEG", quality=FULL_QUALITY)

        thumb = img.copy()
        ratio = THUMB_WIDTH / thumb.width
        thumb = thumb.resize((THUMB_WIDTH, max(1, int(thumb.height * ratio))))
        thumb.save(IMAGES_THUMB_DIR / f"{dest_stem}.jpg", "JPEG", quality=THUMB_QUALITY)
        thumb.save(IMAGES_THUMB_DIR / f"{dest_stem}.webp", "WEBP", quality=THUMB_QUALITY)

    return width, height


def write_stub(
    dest_stem: str,
    journal_slug: str,
    journal_name: str,
    theme_text: str,
    date_str: str,
    date_precision: str,
    issue: str,
    width: int,
    height: int,
) -> None:
    ILLUSTRATIONS_DIR.mkdir(parents=True, exist_ok=True)
    stub_path = ILLUSTRATIONS_DIR / f"{dest_stem}.md"
    if stub_path.exists():
        print(f"  ! Skipping stub, already exists: {stub_path}")
        return

    front_matter = {
        "id": dest_stem,
        "title": "",
        "source_publication": journal_name,
        "source_slug": journal_slug,
        "date": date_str,
        "date_precision": date_precision,
        "date_display": "",
        "issue": issue,
        "theme_tags": [theme_text],
        "caption": "",
        "description": "",
        "artist": "",
        "medium": "",
        "page_number": "",
        "image_file": f"/assets/images/illustrations/full/{dest_stem}.jpg",
        "thumb_file": f"/assets/images/illustrations/thumb/{dest_stem}.jpg",
        "width": width,
        "height": height,
        "rights": "Public Domain",
        "source_scan_note": "",
        "date_added": dt.today().isoformat(),
    }
    content = "---\n" + yaml.dump(
        front_matter, sort_keys=False, allow_unicode=True
    ) + "---\n"
    stub_path.write_text(content, encoding="utf-8")
    print(f"  + Wrote stub: {stub_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Prep a batch of illustrations for the archive.")
    parser.add_argument("folder", type=Path, help="Folder of newly scanned/cropped images")
    parser.add_argument("--journal", required=True, help="Journal slug, must exist in data/journals.yml")
    parser.add_argument("--date", required=True, help="Best-known date: 1883-04-12, 1883-04, or 1883")
    parser.add_argument("--issue", default="", help="Issue/volume label, e.g. no042")
    parser.add_argument("--theme", required=True, help="Theme for this batch, Georgian or Latin (e.g. \u10dd\u10db\u10d8)")
    args = parser.parse_args()

    journals = load_journals()
    if args.journal not in journals:
        sys.exit(f"Unknown journal slug '{args.journal}'. Add it to {JOURNALS_FILE} first.")
    journal_name = journals[args.journal]

    date_parts = args.date.split("-")
    precision = {1: "year", 2: "month", 3: "exact"}.get(len(date_parts), "exact")
    padded_date = args.date + "-01" * (3 - len(date_parts))

    if not args.folder.is_dir():
        sys.exit(f"Not a folder: {args.folder}")

    images = sorted(p for p in args.folder.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS)
    if not images:
        sys.exit(f"No images found in {args.folder}")

    processed_dir = args.folder / "processed"
    processed_dir.mkdir(exist_ok=True)

    theme_slug = slugify(args.theme)
    print(f"Processing {len(images)} image(s) for {journal_name} ({args.date})...")

    for i, src in enumerate(images, start=1):
        seq = f"{i:02d}"
        parts = [args.journal, args.date, args.issue, theme_slug, seq]
        dest_stem = "_".join(p for p in parts if p)

        width, height = process_image(src, dest_stem)
        write_stub(
            dest_stem, args.journal, journal_name, args.theme,
            padded_date, precision, args.issue, width, height,
        )
        shutil.move(str(src), str(processed_dir / src.name))

    print("\nDone. Now open the new files in _illustrations/ and fill in caption, tags, and artist.")


if __name__ == "__main__":
    main()
