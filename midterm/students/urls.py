from django.urls import path
from . import views


urlpatterns = [
    path('', views.StudentView.as_view()),
    path('<int:pk>/', views.StudentDetailsView.as_view()),
]
