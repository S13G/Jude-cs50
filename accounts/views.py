from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dashboard.models import UserProfile
from django.db import transaction
from decimal import Decimal
# Create your views here.
def index(request):
    return render(request,'home/index.html')

@transaction.atomic
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        password_two = request.POST['password2']
        account_list = [10000,100000,1000000]
        if password == password_two:
            account_size = Decimal(request.POST['accountSize'])
            if User.objects.filter(username = username).exists():
                messages.error(request,'Username Already Used')
                return redirect('accounts:register')
            elif account_size not in account_list:
                print("invalid")
                messages.error(request,'Invalid account size')
                return redirect('accounts:register')
            else:
                user = User.objects.create_user(username=username, password=password)
                user_profile = UserProfile(account_size=account_size,user=user,account_balance=account_size)
                user.save();
                user_profile.save();
                messages.success(request,'Account was created successfully')
                return redirect('accounts:login')
            # except:
            #     messages.error(request,'Invalid Inputs')
            #     return redirect('accounts:register')

    return render(request,'accounts/register.html')
# yfinance, django-heroku


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,f'Welcome on board {user.username.capitalize()}')
            return redirect('dashboard:index')
        else:
            messages.error(request,'Invalid Credentials!')
            return redirect('accounts:login')
    return render(request,'accounts/login.html')

@login_required(redirect_field_name="next", login_url="accounts:login")
def logout(request):
    messages.success(request,'Thank you for Coming!')
    auth.logout(request)
    return redirect('accounts:home')
