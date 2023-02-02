from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('register/', views.registerUser, name="register"),
    path ('', views.profiles_view, name='profiles'),
    path ('profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('account/', views.userAccount, name='account'),
    path('edit-account/' ,  views.editAccount, name="edit-account"),
    path('create-skill/', views.createSkill , name="create-skill"),
     
]
