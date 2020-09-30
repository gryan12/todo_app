from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login 
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Todo
from .forms import TodoForm

from .models import validate_user

def home(request):
    return render(request, 'core/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'core/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'core/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'core/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def registeruser(request):

    if request.method == 'GET': 
        return render(request, 'core/registeruser.html', {'form':UserCreationForm()})

    elif request.method == 'POST':
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

        if not user: 
           return render(request, 'core/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('current')

@login_required
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('current')
        except ValueError:
            return render(request, 'core/createtodo.html', {'form':TodoForm(), 'error':'Bad data passed in. Try again.'})

@login_required
def current(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'core/current.html', {'todos':todos})

@login_required
def completed(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'core/completed.html', {'todos':todos})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'core/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('current')
        except ValueError:
            return render(request, 'core/viewtodo.html', {'todo':todo, 'form':form, 'error':'Bad info'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('current')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('current')