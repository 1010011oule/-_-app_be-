from django.contrib.auth import views as auth_views
from django.urls import path
from training import views


urlpatterns = [
    path('', views.homepage, name='homepage'),  # Adjust to your homepage view
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='training/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='homepage'), name='logout'),
    path('levels/<int:level_number>/<str:section_type>/', views.section_detail, name='section_detail'),
    path('levels/', views.level_list, name='level_list'),
    path('sections/<int:section_id>/exercises/<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),
]

