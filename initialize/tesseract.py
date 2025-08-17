import pytesseract
from pdf2image import convert_from_path


def pdfToText(tesseract_dir, poppler_dir, current_dir):
    pytesseract.pytesseract.tesseract_cmd = tesseract_dir

    images = convert_from_path(current_dir, poppler_path=poppler_dir)

    texto_total = ''
    for i, image in enumerate(images):
        texto = pytesseract.image_to_string(image, lang='eng')
        texto_total += f"\n--- Página {i+1} ---\n{texto}"
    return texto_total