from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.home, name='home'),
    path('loan/', views.loan, name='loan'),
    path('currency/', views.currency, name='currency'),
    path('form/', views.form, name='form'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('resultsData/', views.resultsData, name='result'),
    path('stocks/', views.stockPicker, name='stockpicker'),
    path('stocktracker/', views.stockTracker, name='stocktracker'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('table/', views.table, name='table'),
    path('delete/<str:pk>', views.deleteInput, name='delete'),
]
