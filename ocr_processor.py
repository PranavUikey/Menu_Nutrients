# ocr_processor.py
from PIL import Image
import pytesseract

class OCRProcessor:
    def __init__(self):
        # Optional path if you're on Linux or Windows
        pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

    def extract_text(self, image: Image.Image, lang="eng+hin+mar") -> str:
        return pytesseract.image_to_string(image, lang=lang)
