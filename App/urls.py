from django.urls import path

from .views import *

app_name = 'main'
urlpatterns = [
    path('', home_view, name='home'),
    path('inbox/', inbox_view, name='inbox'),
    path('send_message', send_message_view, name='send_message'),
    path('del_message/<int:id>/', delete_message_view, name='del_message'),
    path('customer/<int:id>/', customer_detail_view, name='customer'),
    path('mark_message/', mark_message, name='mark_message'),
    path('email', email, name='email'),
    path('auto_logout/', auto_logout_user, name='auto_logout'),
]

