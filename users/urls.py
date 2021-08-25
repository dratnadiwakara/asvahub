from django.urls import path
from users.views import register

urlpatterns = [
    path("register/<str:ut>/", register, name="register"),
]
