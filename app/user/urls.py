from django.urls import path
from . import views

app_name = 'user'

urlpattrens = [
    path('create/', views.CreateUserView.as_view(), name='create')
]
