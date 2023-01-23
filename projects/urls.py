from django.urls import path
from . import views


urlpatterns =[
    path('', views.projects, name="projects-list"),
    path('detial/<str:pk>/' , views.single_project, name="single-project"),
    path('create-project/', views.createProject, name='create-project'),
    path('update-project/<str:pk>/', views.updateProject, name="update-project"),
    path('delete-project/<str:pk>/', views.deleteProject, name="delete-project"),

    
    ]
