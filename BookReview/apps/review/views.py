from django.shortcuts import render, redirect, HttpResponse
from .models import User, Book, ReviewRate
from django.contrib import messages
from django.core.urlresolvers import reverse
import bcrypt

def index(request):
    return render(request, "index.html")

def books(request):
    user = User.objects.get(id = request.session['uid'])
    reviews = ReviewRate.objects.all().order_by('-created_at')
    books = Book.objects.all()
    context = {
    "user" : user,
    "reviews" : reviews[:3],
    "books" : books
    }
    return render(request, "books.html", context)

def addbooks(request):
    books = Book.objects.all()
    context = {
    "books" : books
    }
    return render(request, "addbooks.html", context)

def postbooks(request):
    booktitle = request.POST['title']
    author = ""
    if 'alist' in request.POST:
        author = request.POST['alist']
    if not author:
        author = str(request.POST['newauthor'])
    review = request.POST['review']
    rating = int(request.POST['rating'])
    books = Book.objects.all()
    for book in books:
        if booktitle == book.title:
            messages.add_message(request, messages.INFO, "Book already exists")
            return redirect('/books/add')
    user = User.objects.get(id = request.session['uid'])
    book = Book.objects.create(title = booktitle, author = author)
    ReviewRate.objects.create(review = review, rating = rating, users = user, books = book)
    return redirect(reverse('show_book', kwargs={'id': book.id }))

def book(request,id):
    book = Book.objects.get(id = id)
    reviews = ReviewRate.objects.filter(books = book)
    context = {
    "book" : book,
    "reviews" : reviews
    }
    return render(request, "bookinfo.html", context)

def postreview(request, id):
    review = request.POST['review']
    rating = int(request.POST['rating'])
    user = User.objects.get(id = request.session['uid'])
    book = Book.objects.get(id = id)
    ReviewRate.objects.create(review = review, rating = rating, users = user, books = book)
    return redirect(reverse('show_book', kwargs={'id': book.id }))

def viewuser(request, id):
    user = User.objects.get(id = id)
    context = {
    "user" : user,
    }
    return render(request, "userinfo.html", context)


def register(request):
    request.session['login'] = False
    print request.session['login']
    fname = str(request.POST['first_name'])
    lname = str(request.POST['last_name'])
    email = str(request.POST['email'])
    pwd = request.POST['password'].encode()
    conpwd = request.POST['confirm_password'].encode()
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
            messages.add_message(request, messages.ERROR, ele)
        return redirect('/')
    else:
        hashedpwd = bcrypt.hashpw(pwd, bcrypt.gensalt())
        user = User.objects.create(first_name = fname, last_name = lname, email = email, password = hashedpwd)
        request.session['uid'] = user.id
        return redirect('/books')

def login(request):
    request.session['login'] = True
    print request.session['login']
    email = str(request.POST['email'])
    pwd = request.POST['password'].encode()
    user = User.objects.all().filter(email = email)
    if  not user:
        messages.add_message(request, messages.INFO, "Email doesn't exist! Please register")
        return redirect('/')
    else:
        if user[0].password != bcrypt.hashpw(pwd, (user[0].password).encode()):
            messages.add_message(request, messages.INFO, "Invalid password")
            return redirect('/')
        else:
            request.session['uid'] = user[0].id
            return redirect('/books')

def logout(request):
    request.session.clear()
    return redirect('/')
