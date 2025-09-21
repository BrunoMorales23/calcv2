from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.contrib import messages
from calcScripts.main import *
#from .models import workQueue
from django.conf import settings

# Create your views here.
def home(request):
    global work_queue, log_path
    if request.method == "GET":
        work_queue, log_path = initializeScripts()
        bbdd_content = workQueue.objects.all().values("id_value", "status", "log").order_by('-id')
        #print(bbdd_content)
        return render(request, "home.html", {"wq": bbdd_content})
    elif request.method == "POST":
        action = request.POST.get("action")
        if action == "cargarWQ":
            archivos = request.FILES.getlist("archivo")
            if archivos:
                for archivo in archivos: 
                    fs = FileSystemStorage()
                    file_name = fs.save(archivo.name, archivo)
                    file_path = fs.path(file_name)
                    wqUpload(work_queue, log_path, file_name, file_path)
                bbdd_content = workQueue.objects.all().values("id_value", "status", "log").order_by('-id')
            return redirect("home")
        elif action == "vaciarWQ":
            bbdd_content = workQueue.objects.all().delete()
            media_root = settings.MEDIA_ROOT
            media_files = os.listdir(media_root)
            for file in media_files:
                os.remove(os.path.join(media_root,file))
        return redirect("home")
    else:
        return render(request, "home.html")

def test(request):
    return render(request, "test.html")

def upload_file(request):
    if request.method == "GET":
        filename = request.GET.get("filename")
        print(filename)
        if filename != None:
            #tener en cuenta el output de Core para poder registrar Logs en algún futuro.
            result = core()
            return render(request, "result.html", {'resultado' : result})
        return render(request, "test.html", {"filename": filename})
    elif request.method == "POST":
        action = request.POST.get("action")
        if action == "iniciar":
            archivos = request.FILES.getlist("archivo")
            print(archivos)
            if archivos:
                for archivo in archivos: 
                    fs = FileSystemStorage()
                    filename = fs.save(archivo.name, archivo)
                return redirect(reverse("upload") + f"?filename={filename}")
            else:
                return redirect(reverse("home"))
        else:
            return redirect(reverse("home"))

def loading(request):
    if request.method == "GET":
        return render(request, "test.html")