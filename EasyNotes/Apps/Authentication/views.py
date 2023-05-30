from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required


def signupaccount(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("home")
        else:
            form = RegisterForm()
        return render(request, 'signupaccount.html', {"form": form})
    else:
        return redirect("userhome")
        

#@login_required       
def logoutaccount(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')
    else:
        return redirect("home")

def loginaccount(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'loginaccount.html',{'form':AuthenticationForm})
        else:
            user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'loginaccount.html',{'form': AuthenticationForm(),'error': 'Incorrect username or password'})
        else:
            login(request,user)
        return redirect('home')
    else:
        return redirect("userhome")