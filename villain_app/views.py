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
    return render(request, "villain.html")

def get_villains(request):
    if request.method == "POST":
        errors = Villain.objects.validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
    villain=Villain.objects.create(
        name = request.POST["name"],
        description = request.POST['description'],
        interests = request.POST['interests'],
        villain_url = request.POST['villain_url'],
        date_added = request.POST["updated_at"],
    )
    return redirect('/villains')

def villain_cards(request):
    if request.method == "GET":
        return redirect("/")
    user=User.objects.all()
    villain=Villain.objects.all()
    context = {
        "all_villains":all_villains,
        "all_users":all_users
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

def add_villain(requesst):
    new_villain=Villain.objects.create(
        name = request.POST["name"],
        description = request.POST['description'],
        interests = request.POST['interests'],
        villain_url = request.POST["villain_url"],
        date_added = request.POST["updated_at"],
        )
    return redirect("/villains")

def delete(request):
    return render(request, 'deletevillain.html')

def delete_villain(request):
    name = request.POST.get("name")
    villain = Villain.objects.filter(name=name.first())
    if villain == villain:
        return redirect(f'/villains')
    return redirect("/")
