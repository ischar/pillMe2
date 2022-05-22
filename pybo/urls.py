from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('login/', auth_views.LoginView.as_view(template_name='pybo/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup, name='signup'),
    path('mypill/', views.mypill, name='mypill'),
    path('friend/', views.friend, name='friend'),
    path('searchFriend/', views.search, name='searchFriend'),
    path('addpill/', views.addpill, name='addpill')
]