# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout_page'),
    path('signup/', views.signup, name='signup'),
    path('passwords/', views.passwords_page, name='passwords_page'),
    path('add-password/', views.add_password_page, name='add_password_page'),
    path('remove-password/', views.remove_password, name='remove_password'),
    path('generate-password/', views.generate_password, name='generate_password'),
    path('encrypt/', views.encrypt_file, name='encrypt_file'),
    path('decrypt/', views.decrypt_file, name='decrypt_file'),
]
