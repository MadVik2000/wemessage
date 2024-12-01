"""
This file contains all the APIs related to group message model.
"""

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from groups.models import Group, GroupMember
from groups.services import create_group_member
from utils.views import CachingAPIView


class JoinGroupAPI(CachingAPIView):
    """
    This API is used to join a group
    """

    permission_classes = (IsAuthenticated,)

    def validate_request(self, group_id: str, user_id: str):
        """
        Checks if groups exists and the user is a member of the group
        """

        if not (group := self.get_cache(key_name=str(group_id), model=Group)):
            group = Group.active_objects.get(id=group_id)
            self.set_cache(key_name=str(group_id), value=group, model=Group)

        GroupMember.active_objects.get(group_id=group_id, user_id=user_id)

    def get(self, request, group_id):
        """
        This method is used to join a group
        """

        try:
            self.validate_request(group_id=group_id, user_id=request.user.uuid)
        except Group.DoesNotExist:
            return Response(
                data={"errors": "Group not found"},
                status=HTTP_400_BAD_REQUEST,
            )
        except GroupMember.DoesNotExist:
            success, group_member = create_group_member(
                group_id=group_id, user_id=request.user.uuid
            )
            if not success:
                return Response(
                    data={"errors": group_member},
                    status=HTTP_400_BAD_REQUEST,
                )

            self.set_cache(
                key_name=f"{group_id}-{request.user.uuid}",
                value=group_member,
                model=GroupMember,
            )

            return Response(
                status=HTTP_200_OK, data={"message": "Joined group successfully"}
            )

        return Response(
            data={"errors": "Group member already exists"},
            status=HTTP_400_BAD_REQUEST,
        )
