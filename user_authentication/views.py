from django.http import HttpResponse
from django.shortcuts import render
from car_seller.models import *
from .forms import *
from django.contrib.auth import login, authenticate

def index(request):
    shelf = CarSeller.objects.all()
    return render(request, 'index.html', {'shelf': shelf})

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username = cd['username'],
                                password = cd['password'])
            if user is not None:
                login(request, user)
                return HttpResponse('Authentication was successfull')
            else:
                return HttpResponse("Invalid username or password.")
        
    form = LoginForm()
    return render(request, "registartion/login.html", {'form':form})


def registration(request):
    pass