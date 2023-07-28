from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def home(request):
    return render(request, 'pages/home.html')
def signup(request):
    return render(request, 'users/signup.html', {
        'form': UserCreationForm()
        }
    )