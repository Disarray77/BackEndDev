
from django.urls import path
from todo_app import views

urlpatterns = [
    path('api/todo-lists', views.todo_lists_handler),
    path('api/todo-lists/<int:pk>', views.todo_list_handler),
    path('api/todo-lists/<int:pk>/todos', views.todo_list_todos_handler),
    path('api/todos', views.todos_handler),
    path('api/todos/<int:pk>', views.todo_handler)
]