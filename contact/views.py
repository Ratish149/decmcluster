from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from account.permissions import IsSuperAdmin

from .models import Contact
from .serializers import ContactSerializer


class ContactListCreateAPIView(ListCreateAPIView):
    queryset = Contact.objects.all().order_by("-created_at")
    serializer_class = ContactSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated(), IsSuperAdmin()]


class ContactDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
