import os
from .initialize import *
from .settings import *
from .initialize.queue import *
from .log import *
from .llama import *
#from gemini import *
#import re
import sys

def core():
    sys.modules['tarfile'] = None
    sys.modules['pickle'] = None


    settings.init()
    work_queue = queue.Queue()

    log_path = setLog()
    ollama = llama.Llama()
    files = getDirContent(settings.inputPath)

    for file in files:
        print(f"Archivo actual: {settings.inputPath}{file}")
        current_dir = os.path.join(settings.inputPath, file)
        content = pdfToText(settings.tesseractPath, settings.popplerPath, current_dir)
        print("--- OCR Run Finished ---")
        queue_id = file.replace(".pdf","")
        work_queue.enqueue(Node(content=content,path=current_dir ,id=queue_id))
        writeLog(log_path, message=f"Item con ID: {queue_id} cargado en cola.")
    
        while work_queue.size() != 0:
            current_item = work_queue.peek()
            item_content = current_item.content
            item_path = current_item.path
            item_id = current_item.id
        
        #LLama
        #------------------------------------------------------------
        llama_template = ollama.getTemplate(settings.promptBase)
        llama_result = ollama.executePrompt(str(llama_template), item_content)
        print(f"{item_id}--- Llama Run Finished ---")
        writeLog(log_path, message=llama_result)
        if os.path.exists(item_path):
            os.remove(item_path)
            #crear lógica de excepción

        llama_result = setEstimation("1", llama_result)
        writeLog(log_path, message=llama_result)
        llama_result = setEstimation("2", llama_result)
        writeLog(log_path, message=llama_result)
        break
    del ollama

    return llama_result
        #------------------------------------------------------------

    #     #Gemini
    #     #------------------------------------------------------------
    #     #gemini_content = gemini.executePrompt(pdf_path=item_path, prompt="Detecta los siguientes puntos y responde de la forma más breve posible, ya sea respondiento por 'Si' o 'No', o bien, declarando la cantidad (en números) de elementos que cumplen con la condición:" \
    #     #"- ¿Es necesario hacer reporte de ejecución?" \
    #     #"- ¿Cuántas aplicaciones/aplicativos/programas son requeridos en la automatización?" \
    #     #"- ")

        #regex_flag = re.search("^¿*?$", gemini_content)
        #if regex_flag == True:
        #    regex_content = re.sub( "(?<=\[)(.*?)(?=\])", "", gemini_content)
        #    print(regex_content)

def setEstimation(pathPrompt, content):
    if pathPrompt == "1":
        pathPrompt = settings.estimation_prompt
    elif pathPrompt == "2":
        pathPrompt = settings.horas_prompt
    ollama = llama.Llama()
    with open(pathPrompt, "r", encoding="utf-8") as f:
        queryValue = f.read()
        ollama.modifyQuery(queryValue)
    llama_template = ollama.getTemplate(settings.promptBase)
    llama_result = ollama.executePrompt(str(llama_template) + queryValue, content)
    del ollama
    return llama_result


#Se separan estas funciones a fin de poder ser utilizadas en casos X desde views.py
def setLog():
    current_log_path = initialize.createDir(settings.logsPath)
    current_log = logs.createNewLog(current_log_path)
    return current_log

def writeLog(current_log, message):
    logs.writeLogValue(current_log, message)