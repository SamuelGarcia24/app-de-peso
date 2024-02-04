from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('register/', reggister, name='reggister'),
    path('login/', loggin, name='login'),
    path('logout/', desloggin, name='logout'),
    path('peso/', peso, name='peso'),
    path('miprogreso/', miprogreso, name='miprogreso'),
    path('api/', get_chart, name='api')
]