"""
This module contains all the v1 urls for the groups app.
"""

from django.urls import path

from groups.apis.v1 import *

urlpatterns = [
    path("", CreateGroupAPI.as_view(), name="create_group"),
    path("<int:group_id>/", UpdateGroupAPI.as_view(), name="update_group"),
    path("message/", CreateGroupMessageAPI.as_view(), name="create_group_message"),
    path("join/", JoinGroupAPI.as_view(), name="join_group"),
]
