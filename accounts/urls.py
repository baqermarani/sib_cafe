from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='user_signup'),
    path('login/', views.LoginView.as_view(), name='user_login'),
    path('logout/', views.LogoutView.as_view(), name='user_logout')
]
