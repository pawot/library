from rest_framework import serializers

from shared.serializers import BaseModelSerializer
from bookcase.models import Author, Publisher, Book, Borrowing
from accounts.models import User


class AuthorSerializer(BaseModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class PublisherSerializer(BaseModelSerializer):
    class Meta:
        model = Publisher
        fields = "__all__"


class BookSerializer(BaseModelSerializer):
    publisher = PublisherSerializer()
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = "__all__"


class BorrowingSerializer(BaseModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"
        read_only_fields = ["returned_at", "user"]

    def validate(self, attrs):
        user_id = self.context["request"].headers.get("x-user-id")
        if not user_id:
            raise serializers.ValidationError("Missing user id.")
        try:
            attrs["user"] = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")
        return attrs

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.book.is_available = False
        instance.book.save()
        return instance


class BorrowingPatchSerializer(BaseModelSerializer):
    class Meta:
        model = Borrowing
        fields = ["returned_at"]

    def update(self, instance, validated_data):
        validated_data["is_archived"] = True
        instance = super().update(instance, validated_data)
        instance.book.is_available = True
        instance.book.save()
        return instance

