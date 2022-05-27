from multiprocessing import AuthenticationError
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages 
from django.db import connection
from django.db.models import Q
from .models import User
from .models import Friend
from .models import PillList
from .models import PillTake
from .models import PillTime

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
    friendlist = Friend.objects.all().order_by('id')

    q = request.user.userId

    if q:
        friendlist = friendlist.filter(userId__icontains=q)
        return render(request, 'pybo/friend.html', {'friendlist': friendlist})
    
    
def search(request):
    blogs = User.objects.all().order_by('id')

    q = request.POST.get('q', '')

    if q:
        blogs = blogs.filter(userId__icontains=q)
        friend = blogs.get(userId=q)        
        friends = Friend()
        friends.userId = request.user.userId
        friends.userName = request.user.userName
        friends.userFriend = friend.userName
        friends.userFriendId = friend.userId  
        friends.save()

        userId = request.user.userId
        friendlist = Friend.objects.all().order_by('id')
        friendlist = friendlist.filter(userId__icontains=userId)
        return render(request, 'pybo/friend.html', {'blogs' : blogs, 'friendlist' : friendlist})
    else:
        userId = request.user.userId
        friendlist = Friend.objects.all().order_by('id')
        friendlist = friendlist.filter(userId__icontains=userId)
        return render(request, 'pybo/friend.html', {'friendlist' : friendlist})


def friendList(request):
    friendlist = Friend.objects.all().order_by('id')

    q = request.user.userId

    if q:
        friendlist = friendlist.filter(userId__icontains=q)
        return render(request, 'pybo/friend.html', {'friendlist': friendlist})


def addpill(request):        
        return render(request, 'pybo/addpill.html', {'pilllist': pilllist})

def mypill(request):
    pilllist = PillList.objects.all()
    
    q = request.user.userId
    if q:
        pilllist = pilllist.filter(PillMaster__icontains=q)        
        return render(request, 'pybo/mypill.html', {'pilllist': pilllist})
def addpillList(request):

    smartpill = PillList()
    smartpill.ModuleNum = request.POST.get('ModuleNum')
    smartpill.PillMaster = request.user.userId
    smartpill.PillName = request.POST.get('PillName')
    smartpill.PillAmount = '0'
    PillEat = request.POST.get('PillEat')
    pillTime = request.POST.get('PillTime')

    if PillEat == "식전":
        smartpill.PillEat = '0'
    else:
        smartpill.PillEat = '1'

    if pillTime == '1':
        smartpill.PillTime = '0'
    elif pillTime == '2':
        smartpill.PillTime = '1'
    else:
        smartpill.PillTime = '2'

    smartpill.save()

    pilltime = PillTime()
    pilltime.ModuleNum = request.POST.get('ModuleNum')
    pilltime.PillName =  request.POST.get('PillName') 
    pilltime.PillMaster = request.user.userId
    pilltime.EatTime = request.POST.get('EatTime')
    pilltime.save()
    
    return render(request, 'pybo/addpill.html')

def friendpill(request, username):
   # pilllist = PillList.objects.all()
    userName = {
        'userName': username,
    }
   # pilllist = pilllist.objects.filter(PillMaster__icontains=userName)

#    render(request, 'pybo/friendpill.html', {'pilllist': pilllist})
    return render(request, 'pybo/friendpill.html', {'userName' : userName})
