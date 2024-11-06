"""
This module contains all the APIs related to group model
"""

from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from groups.services import create_group


class CreateGroupAPI(APIView):
    """
    This API is used to create a group
    """

    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.Serializer):
        """
        This class is used to serializer input parameters for encapsulating API
        """

        name = serializers.CharField()
        description = serializers.CharField()
        image = serializers.ImageField(required=False)

    def post(self, request):
        """
        This method is used to create a group.
        """
        serializer = self.InputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                data={"errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        validated_data = serializer.validated_data
        success, group = create_group(
            name=validated_data["name"],
            description=validated_data["description"],
            image=validated_data.get("image"),
            created_by_id=request.user.uuid,
        )

        if not success:
            return Response(
                data={"errors": group},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            data={
                "name": group.name,
                "description": group.description,
                "image": (group.image or None) and group.image.url,
            },
            status=status.HTTP_201_CREATED,
        )
