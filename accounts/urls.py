from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Custom Sign Up View
    path('signup/', views.signup_view, name='signup'),

    # Built-in Login View
    # We pass 'template_name' so it knows where to find your Tailwind login page
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),

    # Built-in Logout View
    # 'next_page' defines where to go after logging out (usually index or login)
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
]
