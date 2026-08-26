from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Custom Sign Up View
    path('register/', views.register_user, name='register'),

    # Built-in Login View
    # We pass 'template_name' so it knows where to find your Tailwind login page
    path('login/', views.login_user, name='login'),

    # Built-in Logout View
    # 'next_page' defines where to go after logging out (usually index or login)
    path('logout/', views.logout_user, name='logout'),
]
