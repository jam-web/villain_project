from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.

def index(request):
    return render(request, "login.html")

def register(request):
    if request.method == "GET":
        return('/')
    errors = User.objects.validator(request.POST)
    print(errors)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    hash_password = bcrypt.hashpw(
        request.POST['password'].encode(), 
bcrypt.gensalt()).decode()
    new_user = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=hash_password,
    )
    request.session['user.first_name'] = new_user.first_name
    request.session['id'] = new_user.id
    messages.success(request, "You have successfully registered!")
    return redirect('/')

def login(request):
    if request.method == "GET":
        return redirect("/")
    errors = User.objects.log_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['first_name'] = user.first_name
    request.session['last_name'] = user.last_name
    request.session['id'] = user.id
    return redirect("/villains")

def logout(request):
    request.session.flush()
    return redirect('/login')

def villains(request):
    context = {
        "villains":Villain.objects.all()
    }
    return render(request, "villain.html", context)


def add(request):
    if "id" not in request.session:
        return redirect('/')
    users=User.objects.get(id=request.session['id'])
    villains=Villain.objects.filter(id=request.session['id'])
    context = {
        "users":users,
        "villains":villains,
        }
    return render(request, "addvillain.html", context)

def add_villain(request):
    villain = Villain.objects.create(
        name = request.POST['name'],
        description = request.POST["description"],
        interests = request.POST['interests'],
        user_villain = User.objects.get(id=request.session['id']),
        villain_img = request.FILES["villain_img"],
    )
    return redirect('/add')

def delete(request):
    context = {
        "villains":Villain.objects.all()
    }
    return render(request, 'deletevillain.html', context)

def delete_villain(request):
    if request.method == "POST":
        villain=Villain.objects.filter(id = request.POST['villain_id'])
        if len(villain) != 1:
            return redirect("/villains")
        villain[0].delete()
        return redirect("/villains")
    