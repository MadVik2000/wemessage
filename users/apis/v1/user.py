"""
This file contains all the APIs related to user model.
"""

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.views import APIView

from users.services import get_or_create_user


class GenerateUserTokenAPI(APIView):
    """
    This API is used to generate user token.
    """

    permission_classes = (AllowAny,)

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


class CreateUserAPI(APIView):
    """
    This API is used to create user.
    Response Codes:
        201, 400
    """

    permission_classes = (AllowAny,)

    class InputSerializer(serializers.Serializer):
        """
        This serializer is used to validate the input data.
        """

        email = serializers.EmailField()
        username = serializers.CharField()
        password = serializers.CharField()
        first_name = serializers.CharField()
        last_name = serializers.CharField(required=False)
        profile_image = serializers.ImageField(required=False)

    def post(self, request):
        """
        This method is used to create user.
        """

        serializer = self.InputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=HTTP_400_BAD_REQUEST, data=serializer.errors)

        validated_data = serializer.validated_data

        success, user = get_or_create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            password=validated_data["password"],
            last_name=validated_data.get("last_name"),
            profile_image=validated_data.get("profile_image"),
        )

        if not success:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"errors": user},
            )

        return Response(status=HTTP_201_CREATED, data={"token": user.token})
