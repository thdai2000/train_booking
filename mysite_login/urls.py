# from django.conf.urls import url
from django.urls import path
from django.conf.urls import include
from django.contrib import admin
from login.views import index, login, register, logout
from booking.views import userview, adminview, bookingview, QueryView, addview, deleteview


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login),
    path('register/', register),
    path('logout/', logout),
    path('captcha', include('captcha.urls')),
    path('user_index/', userview, name='user'),
    path('admin_index/', adminview, name='admin'),
    path('add/', addview, name='add'),
    path('delete/', deleteview, name='delete'),
    path('booking/', bookingview, name='booking'),
    path('query/', QueryView.as_view(), name='query')
]


