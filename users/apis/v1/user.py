"""
This file contains all the APIs related to user model.
"""

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.views import APIView


class GenerateUserTokenAPI(APIView):
    """
    This API is used to generate user token.
    """

    class InputSerializer(serializers.Serializer):
        """
        This serializer is used to validate the input data.
        """

        email = serializers.EmailField(required=False)
        username = serializers.CharField(required=False)
        password = serializers.CharField()

        def validate(self, attrs):
            if not attrs.get("email") and not attrs.get("username"):
                raise serializers.ValidationError(
                    "Either email or username is required."
                )

            return attrs

    def post(self, request):
        """
        This method is used to generate user token.
        Response Codes:
            200, 400, 404
        """

        serializer = self.InputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=HTTP_400_BAD_REQUEST, data=serializer.errors)

        validated_data = serializer.validated_data
        username = validated_data.get("username")
        email = validated_data.get("email")
        password = validated_data.get("password")

        if username:
            user = authenticate(username=username, password=password)
        else:
            user = authenticate(email=email, password=password)

        if not user:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data={"errors": "Invalid credentials or user not found."},
            )

        return Response(
            status=HTTP_200_OK,
            data={"token": user.token},
        )
