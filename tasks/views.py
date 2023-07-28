from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

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
def tasks(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=True)
    
    return render(request, 'tasks/tasks.html', {'tasks': tasks})
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

    