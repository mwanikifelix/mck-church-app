from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.church.models import DepartmentMember
from apps.hbc.models import HBCMember

from .models import (
    BibleChatMessage,
    BibleChatSession,
    DirectMessage,
    DMThread,
    GroupChatMessage,
    GroupChatThread,
)
from .permissions import DMThreadPermission, GroupChatPermission, OwnBibleChatPermission
from .serializers import (
    BibleChatMessageSerializer,
    BibleChatSessionSerializer,
    DirectMessageSerializer,
    DMThreadSerializer,
    GroupChatMessageSerializer,
    GroupChatThreadSerializer,
)
from .services import generate_bot_reply, get_or_create_dm_thread


class BibleChatSessionViewSet(viewsets.ModelViewSet):
    serializer_class = BibleChatSessionSerializer
    permission_classes = [OwnBibleChatPermission]

    def get_queryset(self):
        return BibleChatSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["get", "post"])
    def messages(self, request, pk=None):
        session = self.get_object()
        if request.method == "POST":
            content = request.data.get("content", "")
            if not content:
                return Response({"detail": "content is required."}, status=status.HTTP_400_BAD_REQUEST)
            BibleChatMessage.objects.create(session=session, is_from_bot=False, content=content)
            bot_message = BibleChatMessage.objects.create(
                session=session, is_from_bot=True, content=generate_bot_reply(content)
            )
            return Response(BibleChatMessageSerializer(bot_message).data, status=status.HTTP_201_CREATED)
        qs = BibleChatMessage.objects.filter(session=session)
        return Response(BibleChatMessageSerializer(qs, many=True).data)


class DMThreadViewSet(viewsets.ModelViewSet):
    serializer_class = DMThreadSerializer
    permission_classes = [DMThreadPermission]
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        user = self.request.user
        return DMThread.objects.filter(Q(user_a=user) | Q(user_b=user))

    def create(self, request, *args, **kwargs):
        other_user_id = request.data.get("user_id")
        if not other_user_id:
            return Response({"detail": "user_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        other_user = User.objects.filter(pk=other_user_id).first()
        if not other_user:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        thread, created = get_or_create_dm_thread(request.user, other_user)
        if thread is None:
            return Response(
                {"detail": "You can only message members who share your HBC or Department."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer(thread)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=["get", "post"])
    def messages(self, request, pk=None):
        thread = self.get_object()
        if request.method == "POST":
            content = request.data.get("content", "")
            if not content:
                return Response({"detail": "content is required."}, status=status.HTTP_400_BAD_REQUEST)
            message = DirectMessage.objects.create(thread=thread, sender=request.user, content=content)
            return Response(DirectMessageSerializer(message).data, status=status.HTTP_201_CREATED)
        qs = DirectMessage.objects.filter(thread=thread)
        return Response(DirectMessageSerializer(qs, many=True).data)


class GroupChatThreadViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only from the API's perspective for thread listing — threads
    themselves are created automatically (one per Department/HBCGroup),
    not user-created."""

    serializer_class = GroupChatThreadSerializer
    permission_classes = [GroupChatPermission]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.has_permission("chat.message_all"):
            return GroupChatThread.objects.all()
        dept_ids = DepartmentMember.objects.filter(user=user).values_list("department_id", flat=True)
        hbc_ids = HBCMember.objects.filter(user=user).values_list("hbc_group_id", flat=True)
        return GroupChatThread.objects.filter(
            Q(department_id__in=dept_ids) | Q(hbc_group_id__in=hbc_ids)
        )

    @action(detail=True, methods=["get", "post"])
    def messages(self, request, pk=None):
        thread = self.get_object()
        if request.method == "POST":
            content = request.data.get("content", "")
            if not content:
                return Response({"detail": "content is required."}, status=status.HTTP_400_BAD_REQUEST)
            message = GroupChatMessage.objects.create(thread=thread, sender=request.user, content=content)
            return Response(GroupChatMessageSerializer(message).data, status=status.HTTP_201_CREATED)
        qs = GroupChatMessage.objects.filter(thread=thread)
        return Response(GroupChatMessageSerializer(qs, many=True).data)
