from rest_framework import serializers


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(
        max_length=1000,
        trim_whitespace=True,
    )

    def validate_message(self, value):
        if not value:
            raise serializers.ValidationError(
                "Please enter a question."
            )

        return value