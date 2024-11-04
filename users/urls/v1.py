"""
This module contains all the v1 urls for the users app.
"""

from django.urls import path

from users.apis.v1 import *

urlpatterns = [
    path("token/", GenerateUserTokenAPI.as_view(), name="generate-user-token"),
]
