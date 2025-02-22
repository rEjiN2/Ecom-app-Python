from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('signupuser/', views.signupuser, name='signupuser'),
    path('loginuser/', views.loginuser, name='loginuser'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'), 
    path('update_profile/', views.update_profile, name='update_profile'), 
    path('update_profile_picture/', views.update_profile_picture, name='update_profile_picture'),
    path('change_password/', views.change_password, name='change_password'),
]