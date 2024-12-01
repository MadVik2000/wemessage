"""
This file contains all the views for the utils app.
"""

from rest_framework.views import APIView

from utils.redis import RedisCacheMixin


class CachingAPIView(APIView, RedisCacheMixin):
    """
    This class extends the APIView class by introducing caching functionalities
    """
