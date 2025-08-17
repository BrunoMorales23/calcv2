from initialize import *
from settings import *

settings.init()
files = getDirContent(settings.inputPath)

for file in files:
    print(f"Archivo actual: {settings.inputPath}{file}")
    current_dir = settings.inputPath+file
    content = pdfToText(settings.tesseractPath, settings.popplerPath, current_dir)
    print(content)