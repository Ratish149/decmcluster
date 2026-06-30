from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import RoleBasedPermission
from decmcluster.pagination import CustomPagination

from .filters import MeetingMinuteFilter
from .models import MeetingMinute
from .serializers import MeetingMinuteSerializer


class MeetingMinuteListCreateAPIView(ListCreateAPIView):
    queryset = (
        MeetingMinute.objects
        .select_related("uploaded_by", "verified_by")
        .prefetch_related("comments", "comments__author")
        .all()
        .order_by("-created_at")
    )
    serializer_class = MeetingMinuteSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = MeetingMinuteFilter
    search_fields = ["name"]
    permission_classes = [IsAuthenticated, RoleBasedPermission]

    def perform_create(self, serializer):
        comment_value = self.request.data.get("comment")
        instance = serializer.save(uploaded_by=self.request.user)
        if comment_value:
            from .models import MeetingMinuteComment

            MeetingMinuteComment.objects.create(
                meeting_minute=instance,
                author=self.request.user,
                comment=comment_value,
            )


class MeetingMinuteDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = (
        MeetingMinute.objects
        .select_related("uploaded_by", "verified_by")
        .prefetch_related("comments", "comments__author")
        .all()
    )
    serializer_class = MeetingMinuteSerializer
    permission_classes = [IsAuthenticated, RoleBasedPermission]

    def perform_update(self, serializer):
        status_value = self.request.data.get("status")

        if status_value == MeetingMinute.StatusChoices.VERIFIED:
            serializer.save(verified_by=self.request.user)
        else:
            serializer.save()


class MeetingMinuteReverifyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        try:
            instance = MeetingMinute.objects.get(pk=pk)
        except MeetingMinute.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if instance.uploaded_by != request.user:
            return Response(
                {"detail": "Only the uploader can resubmit for verification."},
                status=status.HTTP_403_FORBIDDEN,
            )

        instance.status = MeetingMinute.StatusChoices.UNVERIFIED
        instance.verified_by = None
        instance.save()

        comment_value = request.data.get("comment")
        if comment_value:
            from .models import MeetingMinuteComment
            MeetingMinuteComment.objects.create(
                meeting_minute=instance,
                author=request.user,
                comment=comment_value,
            )

        # Resend email to admin
        from .utils import send_meeting_minute_verification_email
        send_meeting_minute_verification_email(instance, comment=comment_value)

        serializer = MeetingMinuteSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

