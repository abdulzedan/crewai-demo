from rest_framework import serializers

class AnalysisSerializer(serializers.Serializer):
    document_text = serializers.CharField(
        required=True,
        help_text="Text of the document to analyze"
    )
    image_url = serializers.URLField(
        required=False,
        help_text="URL of the image to analyze"
    )
    web_query = serializers.CharField(
        required=False,
        help_text="Query for web search"
    )
