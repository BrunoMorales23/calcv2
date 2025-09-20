from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.contrib import messages
from calcScripts.main import *
#from .models import workQueue

# Create your views here.
def home(request):
    if request.method == "GET":
        bbdd_content = workQueue.objects.all().values("id_value", "status", "log").order_by('-id')
        print(bbdd_content)
    return render(request, "home.html", {"wq": bbdd_content})

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
        print(action)
        if action == "iniciar":
            archivo = request.FILES.get("archivo")
            print(archivo)
            if archivo:
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