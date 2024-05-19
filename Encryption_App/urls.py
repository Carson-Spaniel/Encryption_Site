# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.encrypt_file, name='encrypt_file'),
    path('', views.login_page, name='login_page'),
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup, name='signup'),
    path('passwords/', views.passwords_page, name='passwords_page'),
    path('add-password/', views.add_password_page, name='add_password_page'),
    path('encrypt/', views.encrypt_file, name='encrypt_file'),
    path('decrypt/', views.decrypt_file, name='decrypt_file'),
]
