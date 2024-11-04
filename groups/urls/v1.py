"""
This module contains all the v1 urls for the groups app.
"""

from django.urls import path

from groups.apis.v1 import *

urlpatterns = [
    path("", CreateGroupAPI.as_view(), name="create_group"),
]
