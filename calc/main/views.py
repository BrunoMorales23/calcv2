from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, "home.html")

def test(request):
    return render(request, "test.html")

def upload_file(request):
    if request.method == "POST":
        saludo = "AAAAAAAAAAAAAAAAAAAAAAAAAAA"
        return render(request, "test.html", {"filecontent":saludo})