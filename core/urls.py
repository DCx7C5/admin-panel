from django.urls import path, re_path
from core.views import DashboardView, SettingsView, UserProfileView


app_name = 'core'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='profile'),
]
