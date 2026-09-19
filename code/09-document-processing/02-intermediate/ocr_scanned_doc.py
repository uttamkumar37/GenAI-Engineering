# requires pytesseract + the tesseract binary installed (brew install tesseract / apt install tesseract-ocr), and pillow
from __future__ import annotations

import re
from pathlib import Path

import pytesseract
from PIL import Image, ImageDraw, ImageFont

SAMPLE_DIR = Path(__file__).parent / "sample_data"
SCANNED_IMAGE_PATH = SAMPLE_DIR / "scanned_page.png"

SCANNED_TEXT = [
    "ACME CORP - SHIPPING NOTICE",
    "",
    "Order #: 88213",
    "Ship date: 2026-09-12",
    "Contents: 3x Widget Pro, 1x Widget Mini",
    "Please retain this notice for your records.",
]


def make_synthetic_scan(output_path: Path = SCANNED_IMAGE_PATH) -> Path:
    # simulates a scanned document: text rendered to a raster image, no text layer
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (800, 400), color="white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    y = 20
    for line in SCANNED_TEXT:
        draw.text((30, y), line, fill="black", font=font)
        y += 30
    image.save(output_path)
    return output_path


def clean_ocr_text(raw_text: str) -> str:
    lines = [line.strip() for line in raw_text.splitlines()]
    return "\n".join(line for line in lines if line)


def run_ocr(image_path: Path) -> str:
    raw = pytesseract.image_to_string(Image.open(image_path))
    return clean_ocr_text(raw)


if __name__ == "__main__":
    if not SCANNED_IMAGE_PATH.exists():
        make_synthetic_scan()
    text = run_ocr(SCANNED_IMAGE_PATH)
    print(text)
