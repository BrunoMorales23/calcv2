from initialize import *
from settings import *
from queue import *
from log import *
import os

settings.init()
work_queue = queue.Queue()
print(Fore.GREEN +"------------------------------------")
print(Fore.GREEN +"Workqueue Inicializada.")

files = getDirContent(settings.inputPath)

for file in files:
    print(f"Archivo actual: {settings.inputPath}{file}")
    current_dir = os.path.join(settings.inputPath, file)
    content = pdfToText(settings.tesseractPath, settings.popplerPath, current_dir)
    queue_id = file.replace(".pdf","")
    work_queue.enqueue(queue_id)
    print(f"Item con ID: {queue_id} cargado en cola.")
    initialize.createDir(settings.logsPath)
    #print(content)