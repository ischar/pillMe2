from multiprocessing import AuthenticationError
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages 
from django.db import connection
from django.db.models import Q
from .models import User

from .models import *
from .forms import *
# Create your views here.

def index(request):
    return render(request, 'pybo/main.html')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        userId = request.POST['userId'].lower()
        password = request.POST['password']
        try:
            user = user.objects.get(userId=userId)
        except:
            messages.error(request, '회원정보를 찾을 수 없습니다.')
        
        user = authenticate(request, userId=userId, password=password)

        if user is not None:
            messages.success(request, '로그인되었습니다.')
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, '아이디 혹은 비밀번호가 틀렸습니다.')
    return render(request, 'pybo/login.html')

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            
            # userid = form.cleaned_data.get('userId')
            #raw_password = form.cleaned_data.get('password1')
           # user = authenticate(userid=userid, password=raw_password)
            login_user(request.POST)
        else:
            form = UserCreationForm()
    return render(request, 'pybo/signup.html')


def mypill(request):
    return render(request, 'pybo/mypill.html')


def friend(request):
    return render(request, 'pybo/friend.html')
    
    
def searchFriend(request):
    try:
        userId = request.GET.get('kw', '')
        cursor = connection.cursor()
        strSql = "SELECT userId FROM pybo_user WHERE userId = "+"'"+userId+"';"
        result = cursor.execute(strSql)
        friend = cursor.fetchall()
        print(result)
        
        connection.coomit()
        connection.close()
    except:
        connection.rollback()
        print("Failed")
            
    return render(request, 'pybo/friend.html')
    