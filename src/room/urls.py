from django.urls import path

from . import views

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('<slug:slug>/', views.room, name='room'),
    path('<slug:slug>/get_messages/', views.get_messages, name='get_messages'),
    path('send/', views.send_message, name='send_message'),
]