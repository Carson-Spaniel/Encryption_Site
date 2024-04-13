# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.encrypt_file, name='encrypt_file'),
    path('encrypt/', views.encrypt_file, name='encrypt_file'),
    path('decrypt/', views.decrypt_file, name='decrypt_file'),

]
