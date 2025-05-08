from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.create_room, name='create_room'),
    path('<slug:slug>/', views.room, name='room'),
]