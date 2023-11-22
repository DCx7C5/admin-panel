from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import SignUpView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
