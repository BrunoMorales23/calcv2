import os
from initialize import *
from settings import *
from queue import *
from log import *
from llama import *

settings.init()
work_queue = queue.Queue()
current_log_path = initialize.createDir(settings.logsPath)
current_log = logs.createNewLog(current_log_path)
ollama = llama.Llama()

files = getDirContent(settings.inputPath)

for file in files:
    print(f"Archivo actual: {settings.inputPath}{file}")
    current_dir = os.path.join(settings.inputPath, file)
    content = pdfToText(settings.tesseractPath, settings.popplerPath, current_dir)
    queue_id = file.replace(".pdf","")
    work_queue.enqueue(Node(content=content,path=current_dir ,id=queue_id))
    logs.writeLogValue(current_log, f"Item con ID: {queue_id} cargado en cola.")


while work_queue.size() != 0:
    current_item = work_queue.peek()
    item_content = current_item.content
    
    llama_template = ollama.getTemplate(settings.promptBase)
    llama_result = ollama.executePrompt(str(llama_template), item_content)
    #print(llama_result)
    logs.writeLogValue(current_log, llama_result)
    break