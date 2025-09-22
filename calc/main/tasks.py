from celery import shared_task
from .views import llamaExecution, getCurrentItem, ocrExecution, writeOutput
from .models import workQueue

#@shared_task
def run_ocr(item_id, item_path):
    item_content, llama_operation_step = ocrExecution(item_id, item_path)
    bbdd_current_item = getCurrentItem(log="Inicializando Ejecución", status="Ejecutando")
                        
    return {"wq": bbdd_current_item, "step": llama_operation_step, "item_content": item_content}

#@shared_task
def run_llama(item_id, item_path, item_content):
    llama_result, step = llamaExecution(item_id, item_path, item_content)
    workQueue.objects.filter(id_value=item_id, path_value=item_path).update(log="Finalizado el Análisis por IA", status="Ejecutando")

    return {"llama_result": llama_result, "step": step}

#@shared_task
def run_xlsx_phase(llama_result, item_id, item_path):
    step = writeOutput(llama_result, item_id, item_path)
    bbdd_current_item = getCurrentItem(log="Exportación de datos Completada", status="Completado")

    return {"wq": bbdd_current_item, "step": step}