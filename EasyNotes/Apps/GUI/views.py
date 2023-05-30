from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect

def home(request):
    if request.user.is_authenticated:
        return redirect('userhome')
    else:
        return render(request, 'home.html')


def about(request):
    if request.user.is_authenticated:
        return redirect('userhome')
    else:
        return render(request, 'about.html')

def error404(request, exception):
    return render(request, "error_404.html")