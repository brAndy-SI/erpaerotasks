"Module proviging the class for pdf data extracting"

import pathlib
import fitz
import pdfplumber
import PyPDF2
import cv2
from pyzbar.pyzbar import decode

class PDFExtractor:
    """Exstractiong information from pdf file"""

    def __init__(self, file_path: str):
        self.file_path = pathlib.Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"file with path - {self.file_path} not found")

    def extract_text_with_positions(self):
        structure = []
        with pdfplumber.open(self.file_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                words = page.extract_words()
                for word in words:
                    structure.append({
                        "text": word["text"],
                        "x0": word["x0"],
                        "y0": word["top"],
                        "x1": word["x1"],
                        "y1": word["bottom"],
                        "page": page_num + 1
                    })
        return structure

    def extract_metadata(self):
        with open(self.file_path, 'rb') as file:
            pdf = PyPDF2.PdfReader(file)
            metadata = pdf.metadata
            return {key[1:]: value for key, value in metadata.items() if value}

    def extract_barcodes(self):
        barcodes = []
        doc = fitz.open(self.file_path)
        for page_num in range(len(doc)):
            pix = doc.load_page(page_num).get_pixmap()
            image_path = f"temp_page_{page_num}.png"
            pix.save(image_path)
            img = cv2.imread(image_path)
            decoded_objects = decode(img)
            for obj in decoded_objects:
                barcodes.append({
                    "page": page_num + 1,
                    "type": obj.type,
                    "data": obj.data.decode("utf-8"),
                    "position": obj.rect
                })
        return barcodes

    def extract_all(self):
        return {
            "file_name": self.file_path.name,
            "file_size_kb": round(self.file_path.stat().st_size / 1024, 2),
            "metadata": self.extract_metadata(),
            "text_structure": self.extract_text_with_positions(),
            "barcodes": self.extract_barcodes()
        }

if __name__ == "__main__":
    pdf_extractor = PDFExtractor("data/test_task.pdf")
    pdf_info = pdf_extractor.extract_all()

    for key, value in pdf_info.items():
        print(f"{key}: {value}\n")
