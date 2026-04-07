from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('booking/',booking,name='booking'),
    path('bookings_form/<int:id>',bookings_form, name='bookings_form'),
    path('update_booking/<int:id>',update_booking, name='update_booking'),
    path('delete_booking/<int:id>',delete_booking, name='delete_booking'),
    path('history/',history,name='history'),
    path('profile/',profile,name='profile'),
    path('logout/',logout,name='logout'),
    path('support/',support,name='support'),
    path('about/',about,name='about'),
]