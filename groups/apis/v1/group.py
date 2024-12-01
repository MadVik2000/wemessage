"""
This module contains all the APIs related to group model
"""

from django.utils.functional import empty
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from groups.models import Group
from groups.services import create_group, update_group
from utils.views import CachingAPIView


class CreateGroupAPI(CachingAPIView):
    """
    This API is used to create a group
    """

    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.Serializer):
        """
        This class is used to serializer input parameters for encapsulating API
        """

        name = serializers.CharField()
        tag = serializers.CharField()
        description = serializers.CharField()
        image = serializers.ImageField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        """
        This class is used to serializer output parameters for encapsulating API
        """

        class Meta:
            """
            This class defines meta information for output serializer
            """

            model = Group
            fields = ("id", "name", "description", "image")

    def post(self, request):
        """
        This method is used to create a group.
        """
        serializer = self.InputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                data={"errors": serializer.errors},
                status=HTTP_400_BAD_REQUEST,
            )

        validated_data = serializer.validated_data
        success, group = create_group(
            name=validated_data["name"],
            tag=validated_data["tag"],
            description=validated_data["description"],
            image=validated_data.get("image"),
            created_by_id=request.user.uuid,
        )

        if not success:
            return Response(
                data={"errors": group},
                status=HTTP_400_BAD_REQUEST,
            )

        self.set_cache(key_name=str(group.id), value=group, model=Group)
        return Response(
            data=self.OutputSerializer(group).data,
            status=HTTP_201_CREATED,
        )


class UpdateGroupAPI(CachingAPIView):
    """
    This API is used to update a group
    """

    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.Serializer):
        """
        This class is used to serializer input parameters for encapsulating API
        """

        name = serializers.CharField(required=False)
        tag = serializers.CharField(required=False)
        description = serializers.CharField(required=False)
        image = serializers.ImageField(required=False)

    def get_queryset(self, group_id):
        """
        Returns a queryset of group objects filtered by id

        :param int group_id: The id of the group
        :return: A queryset of group objects
        :rtype: QuerySet
        """

        if not (group := self.get_cache(key_name=str(group_id), model=Group)):
            group = Group.active_objects.get(id=group_id)
            self.set_cache(key_name=str(group_id), value=group, model=Group)

        return group

    def put(self, request, group_id):
        """
        This method is used to update a group.
        """

        try:
            group = self.get_queryset(group_id)
        except Group.DoesNotExist:
            return Response(
                data={"errors": "Group not found"},
                status=HTTP_404_NOT_FOUND,
            )

        serializer = self.InputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                data={"errors": serializer.errors},
                status=HTTP_400_BAD_REQUEST,
            )

        validated_data = serializer.validated_data

        success, group = update_group(
            group=group,
            name=validated_data.get("name", empty),
            tag=validated_data.get("tag", empty),
            description=validated_data.get("description", empty),
            image=validated_data.get("image", empty),
            updated_by_id=request.user.uuid,
        )

        if not success:
            return Response(
                data={"errors": group},
                status=HTTP_400_BAD_REQUEST,
            )

        self.set_cache(key_name=str(group.id), value=group, model=Group)
        return Response(
            status=HTTP_200_OK,
        )
