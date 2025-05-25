from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    is_archived = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
