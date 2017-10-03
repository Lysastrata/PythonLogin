from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from models import User
def index(request):
    return render(request, 'logreg/index.html')
def success(request):
    return render(request, 'logreg/success.html')
def register(request):
    errors = User.objects.basic_validator(request.POST)
    entered = User.objects.filter(email=request.POST['email'])
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        if entered.count() > 0:
            messages.error(request, "email already taken", extra_tags="email")
            return redirect('/')
        else:
            new = User.objects.create(name = request.POST['name'], alias = request.POST['alias'], email = request.POST['email'], password = hashed_pw, birthday = request.POST['birth'])
            request.session['name'] = new.name
            request.session['id'] = "new.id"
            return redirect('/success')
def login(request):
    entered = User.objects.filter(email=request.POST['email'])
    if entered.count() > 0:
        entered = entered.first()
        if bcrypt.checkpw(request.POST['password'].encode(), entered.password.encode()) == True:
            request.session['name'] = entered.name
            request.session['id'] = entered.id
            return redirect('/success')
        else:
            messages.error(request, "Please check password or register", extra_tags="email")
            return redirect('/')
    else:
        messages.error(request, "Please check email or register", extra_tags="email")
        return redirect('/')
