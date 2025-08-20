import os
from initialize import *
from settings import *
from queue import *
from log import *
from llama import *
from gemini import *
import re

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
    item_path = current_item.path
    
    #LLama
    #------------------------------------------------------------
    llama_template = ollama.getTemplate(settings.promptBase)
    llama_result = ollama.executePrompt(str(llama_template), item_content)
    print(llama_result)
    logs.writeLogValue(current_log, llama_result)
    #------------------------------------------------------------

    #Gemini
    #------------------------------------------------------------
    #gemini_content = gemini.executePrompt(pdf_path=item_path, prompt="Detecta los siguientes puntos y responde de la forma más breve posible, ya sea respondiento por 'Si' o 'No', o bien, declarando la cantidad (en números) de elementos que cumplen con la condición:" \
    #"- ¿Es necesario hacer reporte de ejecución?" \
    #"- ¿Cuántas aplicaciones/aplicativos/programas son requeridos en la automatización?" \
    #"- ")

    #regex_flag = re.search("^¿*?$", gemini_content)
    #if regex_flag == True:
    #    regex_content = re.sub( "(?<=\[)(.*?)(?=\])", "", gemini_content)
    #    print(regex_content)
    break