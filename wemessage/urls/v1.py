"""
This module contains all the v1 urls for the wemessage project.
"""

from django.urls import include, path

urlpatterns = [
    path("users/", include("users.urls.v1")),
    path("groups/", include("groups.urls.v1")),
]
