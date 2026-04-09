from django.urls import path
from .views import *

urlpatterns = [
    path('',register,name='register'),
    path('login_/',login_,name='login_'),
    path('logout_/',logout_,name='logout_'),
    path('reset_pass/',reset_pass,name='reset_pass'),
    path('profile/',profile,name='profile'),
    path('forgot_pass/',forgot_pass,name='forgot_pass'),
    path('new_pass/',new_pass,name='new_pass'),
    path('activate/<uidb64>/<token>/', verify_email, name='activate')
    
]
