import os
from .initialize import *
from .settings import *
from .initialize.queue import *
from .log import *
from .llama import *
#from gemini import *
#import re
import sys
from openpyxl import load_workbook
import re
from openpyxl.styles import Font, PatternFill, Alignment
def core():
    sys.modules['tarfile'] = None
    sys.modules['pickle'] = None


    settings.init()
    work_queue = queue.Queue()

    log_path = setLog()
    #ollama = llama.Llama()
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
        ollama = llama.Llama(content=item_content)
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

        writeOutput(llama_result, item_id)
        writeLog(log_path, message=f"Estimación PDD {item_id}.xlsx --- Creado")
        del ollama
        break
    #del ollama

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
    ollama = llama.Llama(content=content)
    with open(pathPrompt, "r", encoding="utf-8") as f:
        queryValue = f.read()
        ollama.modifyQuery(queryValue)
    llama_template = ollama.getTemplate(settings.estimation_prompt)
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

def writeOutput(llama_result, queue_itemID):

    current_row = 3
    current_value = 0
    workBook = load_workbook(settings.template_xlsx_output)
    workSheet = workBook.active

    splittedLines = [p.strip() for p in llama_result.split("Paso") if p.strip()]
    regex_tittle = r"\]: (.*?) . Estimación:"
    regex_horas = r"Estimación:\s*(.*?)(?:\s*Paso|$)"

    for line in splittedLines:
        task_tittle = re.findall(regex_tittle, line)
        if task_tittle == None or task_tittle == "":
            regex_tittle = r"\]:\s*(.*?)\s*\. Estimación:"
            task_tittle = re.findall(regex_tittle, line)
        task_time = re.findall(regex_horas, line)
        print(task_tittle)

        fill = PatternFill(start_color="E6E6E6", end_color="E6E6E6", fill_type="solid")

        cell_b = workSheet[f"B{current_row}"]
        cell_c = workSheet[f"C{current_row}"]

        cell_b.value = task_tittle[0] if task_tittle else ""
        cell_c.value = task_time[0] if task_time else ""

        cell_b.alignment = Alignment(horizontal='center', vertical='center')
        cell_c.alignment = Alignment(horizontal='center', vertical='center')
        cell_b.font = Font(name='Calibri', size=11, color="000000")
        cell_c.font = Font(name='Calibri', size=11, color="000000")

        if current_row % 2 == 0:
            cell_b.fill = fill
            cell_c.fill = fill

        current_row += 1
        current_value += 1

    workBook.save(f"Estimación PDD {queue_itemID}.xlsx")