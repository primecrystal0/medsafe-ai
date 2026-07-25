"""
OCR service — extracts medicine-label text from a photo.

Pipeline: PIL (fix EXIF rotation) -> OpenCV (grayscale, denoise,
adaptive threshold, deskew) -> Tesseract (text extraction).
Runs entirely locally — the raw image never leaves this machine.
"""
import io
import logging

import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageOps

logger = logging.getLogger(__name__)

MAX_IMAGE_DIMENSION = 2000  # px — avoids OOM on huge phone photos

# On Windows, pytesseract usually can't find tesseract.exe automatically.
# Uncomment and adjust this line if you hit a "TesseractNotFoundError":
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class OCRError(Exception):
    """Raised when OCR cannot produce usable text."""


def _load_as_bgr(image_bytes: bytes) -> np.ndarray:
    """Decode bytes into an OpenCV BGR image, respecting EXIF rotation."""
    try:
        pil_image = Image.open(io.BytesIO(image_bytes))
    except Exception as exc:
        raise OCRError(f"Could not read image file: {exc}") from exc

    pil_image = ImageOps.exif_transpose(pil_image)
    if max(pil_image.size) > MAX_IMAGE_DIMENSION:
        pil_image.thumbnail((MAX_IMAGE_DIMENSION, MAX_IMAGE_DIMENSION))

    rgb_array = np.array(pil_image.convert("RGB"))
    return cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)


def _deskew(gray: np.ndarray) -> np.ndarray:
    """Straighten a slightly tilted label photo."""
    coords = np.column_stack(np.where(gray < 255))
    if coords.size == 0:
        return gray

    angle = cv2.minAreaRect(coords)[-1]
    angle = -(90 + angle) if angle < -45 else -angle
    if abs(angle) < 0.5:
        return gray

    (h, w) = gray.shape
    matrix = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    return cv2.warpAffine(
        gray, matrix, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
    )


def _preprocess(image_bytes: bytes) -> np.ndarray:
    """OpenCV pipeline tuned for photographed (not scanned) labels."""
    bgr = _load_as_bgr(image_bytes)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    thresholded = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, blockSize=31, C=15,
    )
    return _deskew(thresholded)


def extract_text(image_bytes: bytes) -> str:
    """Run OCR on raw image bytes and return cleaned text."""
    processed = _preprocess(image_bytes)

    try:
        raw_text = pytesseract.image_to_string(processed)
    except pytesseract.TesseractNotFoundError as exc:
        raise OCRError(
            "Tesseract is not installed on this machine. "
            "Install it and make sure it's on your PATH."
        ) from exc

    cleaned = "\n".join(
        line.strip() for line in raw_text.splitlines() if line.strip()
    )

    if len(cleaned) < 3:
        raise OCRError(
            "Couldn't read any text on that label. Try a clearer, well-lit photo."
        )

    logger.info("OCR extracted %d characters", len(cleaned))
    return cleaned