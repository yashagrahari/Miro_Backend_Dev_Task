from django.urls import path
from .views import UserSignUpView, UserLoginView

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='user-signup'),
    path('login/', UserLoginView.as_view(), name='user-login'),
]
