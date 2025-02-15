from rest_framework import serializers

class ChatSerializer(serializers.Serializer):
    message = serializers.CharField(required=True, max_length=1024)
