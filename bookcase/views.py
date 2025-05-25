from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django_filters.rest_framework import DjangoFilterBackend
from uuid import UUID

from bookcase.models import Book, Borrowing, Author, Publisher
from bookcase.serializers import BookSerializer, BorrowingSerializer, BorrowingPatchSerializer, AuthorSerializer, PublisherSerializer
from bookcase.permissions import IsAdminOrAuthenticatedReadOnly


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrAuthenticatedReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["authors", "is_available"]


class BorrowingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrAuthenticatedReadOnly]
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["book", "user", "is_archived"]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        user = self.request.user
        return Borrowing.objects.all() if user.is_staff else Borrowing.objects.filter(user=user)

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return BorrowingPatchSerializer
        return BorrowingSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(name="x-user-id", type=UUID, location=OpenApiParameter.HEADER, required=True),
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class AuthorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrAuthenticatedReadOnly]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class PublisherViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrAuthenticatedReadOnly]
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
