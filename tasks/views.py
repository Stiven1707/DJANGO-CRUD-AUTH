from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
                return redirect('home')
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