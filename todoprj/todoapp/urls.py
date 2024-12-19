from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('login/', views.login_view, name='login'),
    path('todo/', views.todo_index, name='todo_index'),
    path('register/', views.register, name='register'),
    path('todo/complete/<int:id>/', views.complete_task, name='todo_complete'),
    path('todo/delete/<int:id>/', views.delete_task, name='todo_delete'),
    path('test/', views.test_view, name='test_view'),
]