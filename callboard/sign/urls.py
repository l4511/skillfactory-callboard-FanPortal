from django.urls import path
from .views import RegisterUser, LoginUser, logout_user, check_code

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('register/code/', check_code, name='code'),
    path('login/', LoginUser.as_view(template_name='sign/login.html'), name='login'),
    path('logout/', logout_user, name='logout'),
]
