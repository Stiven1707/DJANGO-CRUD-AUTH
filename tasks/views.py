
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.utils import timezone

from .models import Task

from .forms import TaskForm

# Create your views here.
def home(request):
    return render(request, 'pages/home.html')
def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'users/signup.html', {
                    'form': UserCreationForm(),
                    'error': 'Username has already been taken'
                    }
                )
            except User.DoesNotExist:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1']
                )
                login(request, user)
                return redirect('tasks')
        else:
            return render(request, 'users/signup.html', {
                'form': UserCreationForm(),
                'error': 'Passwords did not match'
                }
            )
    else:
        return render(request, 'users/signup.html', {
            'form': UserCreationForm()
            
            }
        )
@login_required
def signout(request):
    logout(request)
    return redirect('home')
def signin(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            return render(request, 'users/signin.html', {
                'form': AuthenticationForm(),
                'error': 'Username or password did not match'
                }
            )
        else:
            login(request, user)
            return redirect('tasks')
    else:
        return render(request, 'users/signin.html',{'form': AuthenticationForm()})
@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=True)
    
    return render(request, 'tasks/tasks.html', {'tasks': tasks})
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'tasks/tasks.html', {'tasks': tasks})
@login_required
def create_task(request):
    if request.method == 'POST':
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks/create_task.html', {
                'form': TaskForm(),
                'error': 'Bad data passed in. Try again'
                }
            )
    else:
        return render(request, 'tasks/create_task.html', {
        'form': TaskForm()
        }
    )
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'tasks/task_detail.html', {
            'task': task,
            'form': form
            }
        )
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks/task_detail.html', {
                'task': task,
                'form': form,
                'error': 'Bad info'
                }
            )
@login_required
def complete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        task.date_completed = timezone.now()
        task.save()
        return redirect('tasks')
@login_required
def delete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        task.delete()
        return redirect('tasks')