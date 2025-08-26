from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.urls import reverse

# Create your views here.
def home(request):
    return render(request, "home.html")

def test(request):
    return render(request, "test.html")

def upload_file(request):
    if request.method == "GET":
        filename = request.GET.get("filename")
        return render(request, "test.html", {"filename": filename})
    elif request.method == "POST":
        action = request.POST.get("action")
        if action == "iniciar":
            return redirect(reverse("loading"))
        archivo = request.FILES.get("archivo")
        if archivo:
            fs = FileSystemStorage()
            filename = fs.save(archivo.name, archivo)
            return redirect(reverse("upload") + f"?filename={filename}")
        else:
            return redirect(reverse("home"))

def loading(request):
    if request.method == "GET":
        return render(request, "loading.html")