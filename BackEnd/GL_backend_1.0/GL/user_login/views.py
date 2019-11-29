from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.http import HttpResponse

# Create your views here.
def index(request):
    pass
    return render(request, 'login/index.html')

 
def login(request):
    pass
    return render(request, 'login/login.html')
 
 
def register(request):
    pass
    return render(request, 'login/register.html')
 
 
def logout(request):
    pass
    return redirect("/index/")