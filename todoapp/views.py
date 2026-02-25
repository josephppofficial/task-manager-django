from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Task

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'todoapp/login.html', {'error': 'Invalid username or password'})
    return render(request, 'todoapp/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/login/')
def index(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'todoapp/index.html', {'tasks': tasks})

@login_required(login_url='/login/')
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Task.objects.create(title=title, user=request.user)
    return redirect('index')

@login_required(login_url='/login/')
def complete_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('index')

@login_required(login_url='/login/')
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.delete()
    return redirect('index')