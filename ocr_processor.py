from PIL import Image
import pytesseract

# Optional: Linux-specific Tesseract path
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

class OCRProcessor:
    def __init__(self, lang="eng+hin+mar"):
        self.lang = lang

    def extract_text(self, image: Image.Image) -> str:
        return pytesseract.image_to_string(image, lang=self.lang)
