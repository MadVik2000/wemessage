"""
This file contains all the APIs related to group message model.
"""

from django.conf import settings
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from groups.models import Group, GroupMember
from utils.kafka_mixins import BaseKafkaProducer
from utils.redis import RedisCacheMixin


class CreateGroupMessageAPI(APIView, RedisCacheMixin):
    """
    This API is used to create a group message.
    """

    permission_classes = (IsAuthenticated,)
    kafka_producer = BaseKafkaProducer()

    class InputSerializer(serializers.Serializer):
        """
        This class is used to serializer create group message API request body.
        """

        group_id = serializers.IntegerField()
        message = serializers.CharField()

    def validate_request(self, group_id: str, user_id: str):
        """
        Checks if the user is a member of the group
        """

        if not (group := self.get_cache(group_id, Group)):
            group = Group.active_objects.get(id=group_id)
            self.set_cache(group_id, group, Group)

        if not (group_member := self.get_cache(f"{group_id}-{user_id}", GroupMember)):
            group_member = GroupMember.active_objects.get(
                group_id=group_id, user_id=user_id
            )
            self.set_cache(f"{group_id}-{user_id}", group_member, GroupMember)

    def post(self, request):
        """
        This method is used to create a group message.
        """

        serializer = self.InputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=HTTP_400_BAD_REQUEST, data=serializer.errors)

        validated_data = serializer.validated_data

        try:
            self.validate_request(
                group_id=validated_data["group_id"], user_id=request.user.uuid
            )
        except Group.DoesNotExist:
            return Response(
                data={"errors": "Group not found"},
                status=HTTP_400_BAD_REQUEST,
            )
        except GroupMember.DoesNotExist:
            return Response(
                data={"errors": "Group member not found"},
                status=HTTP_400_BAD_REQUEST,
            )

        self.kafka_producer.send_message(
            topic=settings.MESSAGE_CONSUMER_TOPIC,
            value={
                "group_id": validated_data["group_id"],
                "message": validated_data["message"],
                "user_id": str(request.user.uuid),
                "created_at": now().isoformat(),
            },
            key=str(validated_data["group_id"]),
        )

        return Response(status=HTTP_200_OK, data={"message": "Message sent"})
