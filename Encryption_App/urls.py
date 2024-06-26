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
    path('remove-all-passwords/', views.remove_all_passwords, name='remove_all_passwords'),
    path('messages/', views.messages_page, name='messages_page'),
    path('add-message/', views.add_message_page, name='add_message_page'),
    path('remove-message/', views.remove_message, name='remove_message'),
    path('remove-all-messages/', views.remove_all_messages, name='remove_all_messages'),
    path('generate-username/', views.generate_username, name='generate_username'),
    path('generate-password/', views.generate_password, name='generate_password'),
    path('generate_passphrase/', views.generate_passphrase, name='generate_passphrase'),
    path('generate_pin/', views.generate_pin, name='generate_pin'),
    path('encrypt/', views.encrypt_file, name='encrypt_file'),
    path('decrypt/', views.decrypt_file, name='decrypt_file'),
    path('check-data-leak/', views.check_data_leak, name='check_data_leak'),

]
