from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', views.home, name='home'),  # Homepage
    path('profile/', views.profile, name='profile'),
    path('set-budget/', views.set_budget, name='set_budget'),
    path('budget_notification/', views.budget_notification, name='budget_notification'),
    path('financial_dashboard/', views.financial_dashboard, name='financial_dashboard'),
    path('profile/edit/', views.edit_username, name='edit_username'),
    path('change-password/', views.change_password, name='change_password'), 
    #path('set_budget/', views.set_budget, name='set_budget'), 
    path('budget_alerts/', views.budget_alerts, name='budget_alerts'),
    path('add_expenses/', views.add_expenses, name='add_expenses'),
    path('view_expenses/', views.view_expenses, name='view_expenses'),
    path('get_categories/', views.get_categories, name='get_categories'),
    path('filter_expenses/', views.filter_expenses, name='filter_expenses'),  # Add this line
    path('edit_expense/<int:expense_id>/', views.edit_expense, name='edit_expense'),  # New URL for editing an expense
    path('delete_expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('financial_reports/', views.financial_reports, name='financial_reports'),
    #path('set-budget/', views.set_budget, name='set_budget'),
]