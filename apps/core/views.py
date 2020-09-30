from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login 


from .models import validate_user

# Create your views here.

def registeruser(request):

    if request.method == 'GET': 
        return render(request, 'core/registeruser.html', {'form':UserCreationForm()})

    elif request.method == 'POST':
        ##validate first

        if not validate_user(request.POST['username'],request.POST['password1'], request.POST['password2']):
            return render(request, 'core/registeruser.html', {'form':UserCreationForm(), 'error':'Passwords do not match'})

        try:
            user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
            user.save()
            login(request, user)
            return redirect('current')
        except IntegrityError: 
            return render(request, 'core/registeruser.html', {'form':UserCreationForm(), 'error': 'User already registered'})

def login_user(request):
    if request.method == "GET":
        context = {'form':AuthenticationForm()}
        return render(request, 'core/loginuser.html', context)

    elif request.method == "POST":
        user = authenticate(request, username=request.POST['username'], pasword=request.POST['password'])



def current(request):
    return render(request, 'core/current.html')

