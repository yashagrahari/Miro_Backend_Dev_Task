from django.urls import path
from .views import UserSignUpView, UserLoginView

urlpatterns = [
    path('auth/signup/', UserSignUpView.as_view(), name='user-signup'),
    path('auth/login/', UserLoginView.as_view(), name='user-login'),
]
