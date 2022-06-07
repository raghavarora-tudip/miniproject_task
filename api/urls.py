from django.urls import path
from .views import *
urlpatterns = [
    path('create/', CreateAccount.as_view(), name="create_user"),
    path('login/', LoginView.as_view(), name="login"),
    path('users/', ListUsers.as_view(), name="users"),
    path('update/', UpdateProfile.as_view(), name="update"),

]
