# base/urls.py
# REPLACE ENTIRE FILE with this complete URL configuration

from django.urls import path
from . import views

urlpatterns = [
    # ========== EXISTING AUTHENTICATION URLS ==========
    path('', views.home, name='home'),  # Home page
    path('login/', views.login_view, name='login'),  # Login page
    path('register/', views.register_view, name='register'),  # Register page
    path('logout/', views.logout_view, name='logout'),  # Logout (if you have this)
    
    # ========== QUIZ TAKING URLS ==========
    path('select-quiz/', views.select_quiz, name='select_quiz'),
    path('start-quiz/', views.start_quiz, name='start_quiz'),
    path('take-quiz/', views.take_quiz, name='take_quiz'),
    path('save-answer/', views.save_answer, name='save_answer'),
    path('previous-question/', views.previous_question, name='previous_question'),
    path('submit-quiz/', views.submit_quiz, name='submit_quiz'),
    path('quiz-result/<int:quiz_id>/', views.quiz_result, name='quiz_result'),
    path('get-subtopics/<int:topic_id>/', views.get_subtopics, name='get_subtopics'),
    
    # ========== DASHBOARD URLS ==========
    # User Dashboard URLs
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('quiz-history/', views.quiz_history, name='quiz_history'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    
    # Admin Dashboard URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/', views.manage_users, name='manage_users'),
    path('admin/user/<int:user_id>/', views.user_performance, name='user_performance'),
    path('admin/questions/', views.manage_questions, name='manage_questions'),
]