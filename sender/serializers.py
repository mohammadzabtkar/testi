from rest_framework import serializers
from sender.models import SenderAddress

class CompleteSenderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SenderAddress
        fields = ["address", "lat", "long"]
