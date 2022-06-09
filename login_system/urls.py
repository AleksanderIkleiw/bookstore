from django.urls import path
from .views import login_view, register_view, logout_view, activate_view


urlpatterns = [
    path('login/', login_view, name="login_page"),
    path('register/', register_view, name="register_page"),
    path('logout/', logout_view, name='logout_page'),
    path('activate/<str:base64_string>', activate_view, name='activate_page')
]
