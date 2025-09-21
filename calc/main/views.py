from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from calcScripts.main import *
from django.conf import settings as django_settings

request_flush_required = True

def home(request):
    global request_flush_required
    if request_flush_required == True:
        request.session.flush()
        print("--- Session Flush ---")
        request_flush_required = False
    startUpVars(request)
    if request.method == "GET":
        if request.session["llama_operation_flag"] == True:
                match request.session["llama_operation_step"]:
                    case 0:
                        print("CASE 0")
                        #current_item = request.session["work_queue"].peek()
                        work_queue = request.session.get("work_queue", [])
                        current_item = work_queue.pop(0)
                        request.session["item_path"] = current_item["path"]
                        request.session["item_id"] = current_item["id"]
                        request.session["llama_operation_step"] = 1
                        request.session["work_queue"] = work_queue
                        return redirect("home")
                    case 1:
                        print("CASE 1")
                        request.session["item_content"], request.session["llama_operation_step"] = ocrExecution(request.session["item_id"], request.session["item_path"])
                        request.session["bbdd_current_item"] = getCurrentItem(log="Inicializando Ejecución", status="Ejecutando")
                        return render(request, "home.html", {"wq": request.session["bbdd_content"], "currentItem": request.session["bbdd_current_item"]})
                    case 2:
                        print("CASE 2")
                        request.session["llama_result"], request.session["llama_operation_step"] = llamaExecution(request.session["item_id"], request.session["item_path"], request.session["item_content"])
                        request.session["bbdd_current_item"] = getCurrentItem(log="Finalizado el Análisis por IA", status="Ejecutando")
                        return render(request, "home.html", {"wq": request.session["bbdd_content"], "currentItem": request.session["bbdd_current_item"]})
                    case 3:
                        print("CASE 3")
                        request.session["llama_operation_step"] = writeOutput(request.session["llama_result"], request.session["item_id"], request.session["item_path"])
                        request.session["bbdd_current_item"] = getCurrentItem(log="Exportación de datos Completada", status="Completado")
                        return render(request, "home.html", {"wq": request.session["bbdd_content"], "currentItem": request.session["bbdd_current_item"]})
                    case _:
                        raise Exception("Out of Range: 'llama_operation_step' phase.")
        if request.session["initialize_flag"] == True:
            request.session["work_queue"] = initializeScripts()
            request.session["initialize_flag"] = False
        request.session["bbdd_content"] = list(workQueue.objects.all().values("id_value", "status", "log").order_by('-id'))
        return render(request, "home.html", {"wq": request.session["bbdd_content"], "currentItem": request.session["bbdd_current_item"]})
    
    elif request.method == "POST":
        action = request.POST.get("action")

        match action:
            case "cargarWQ":
                if request.session["work_queue"] is None:
                    request.session["work_queue"] = initializeScripts()
                archivos = request.FILES.getlist("archivo")
                if archivos:
                    for archivo in archivos: 
                        fs = FileSystemStorage()
                        file_name = fs.save(archivo.name, archivo)
                        file_path = fs.path(file_name)
                        request.session["work_queue"] = wqUpload(request.session["work_queue"], file_name, file_path)
                    request.session["bbdd_content"] = list(workQueue.objects.all().values("id_value", "status", "log").order_by('-id'))
                    print(len(request.session["work_queue"]))
                return redirect("home")
            case "vaciarWQ":
                request.session["bbdd_content"] = list(workQueue.objects.all().delete())
                media_root = django_settings.MEDIA_ROOT
                media_files = os.listdir(media_root)
                for file in media_files:
                    os.remove(os.path.join(media_root,file))
                #request.session["work_queue"] = Queue()
                request.session["work_queue"] = []
                return redirect("home")
            case "iniciar":
                request.session["llama_operation_flag"] = True

                return redirect("home")
            case _:
                return redirect("home")
            
    else:
        return render(request, "home.html")
    
def startUpVars(request):
    if "llama_operation_flag" not in request.session:
        request.session["llama_operation_flag"] = False
    if "llama_operation_step" not in request.session:
        request.session["llama_operation_step"] = 0
    if "work_queue" not in request.session:
        request.session["work_queue"] = []
    if "item_path" not in request.session:
        request.session["item_path"] = None
    if "item_id" not in request.session:
        request.session["item_id"] = None
    if "item_content" not in request.session:
        request.session["item_content"] = None
    if "bbdd_current_item" not in request.session:
        request.session["bbdd_current_item"] = None
    if "initialize_flag" not in request.session:
        request.session["initialize_flag"] = True
    if "llama_result" not in request.session:
        request.session["llama_result"] = None
    if "bbdd_content" not in request.session:
        request.session["bbdd_content"] = list(workQueue.objects.all().values("id_value", "status", "log").order_by('-id'))
    