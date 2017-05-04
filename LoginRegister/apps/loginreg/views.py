from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "index.html")

def success(request):
    return render(request, "success.html")

def register(request):
    fname = str(request.POST['first_name'])
    lname = str(request.POST['last_name'])
    email = str(request.POST['email'])
    pwd = request.POST['password']
    conpwd = request.POST['confirm_password']
    context = {
    "fname" : fname,
    "lname" : lname,
    "email" : email,
    "pwd" : pwd,
    "conpwd" : conpwd
    }
    if  User.objects.all().filter(email = email):
        messages.add_message(request, messages.INFO, "Email already exists! Please login")
        return redirect('/')
    error = User.objects.validate(context)
    if error:
        for ele in error:
            msgs.add_message(request, messages.ERROR, ele)
        return redirect('/')
    else:
        user = User.objects.create(first_name = fname, last_name = lname, email = email, password = pwd)
        return redirect('/success')

def login(request):
    print User.objects.all()
    email = str(request.POST['email'])
    pwd = str(request.POST['password'])
    user = User.objects.all().filter(email = email)
    if  not user:
        messages.add_message(request, messages.INFO, "Email doesn't exist! Please register")
        return redirect('/')
    else:
        if user[0].password != pwd:
            messages.add_message(request, messages.INFO, "Invalid password")
            return redirect('/')
        else:
            request.session['uid'] = user[0].id
            return redirect('/success')


def logout(request):
    request.session.clear()
    return redirect('/')
