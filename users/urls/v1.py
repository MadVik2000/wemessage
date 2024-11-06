"""
This module contains all the v1 urls for the users app.
"""

from django.urls import path

from users.apis.v1 import *

urlpatterns = [
    path("", CreateUserAPI.as_view(), name="create-user"),
    path("token/", GenerateUserTokenAPI.as_view(), name="generate-user-token"),
]
