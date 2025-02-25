from rest_framework import serializers


class ChatSerializer(serializers.Serializer):
    message = serializers.CharField(required=True, max_length=1024)


class AnalysisQuerySerializer(serializers.Serializer):
    query = serializers.CharField(
        required=True,
        max_length=1024,
        help_text="The search query for the research workflow.",
    )
