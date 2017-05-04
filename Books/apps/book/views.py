from django.shortcuts import render, redirect, HttpResponse
from .models import Books

def index(request):
    context = {
    "books": Books.objects.all()
    }
    return render(request, "index.html", context)

def process(request):
    Books.objects.create(title = request.POST['title'], category = request.POST['category'], author = request.POST['author'])
    return redirect('/')
