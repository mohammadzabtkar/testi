from rest_framework import serializers
from courier.models import Courier

class CompleteCourierProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = [
            "phone_number", "vehicle_type", "vehicle_name",
            "vehicle_country_number", "vehicle_first_number",
            "vehicle_alphabet", "vehicle_second_number"
        ]