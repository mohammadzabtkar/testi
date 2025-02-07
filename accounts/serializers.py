from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    app_type = serializers.ChoiceField(choices=[('courier', 'Courier'), ('sender', 'Sender')])

    class Meta:
        model = User
        fields = ("phone_number", "password", "app_type")

    def create(self, validated_data):
        app_type = validated_data.pop('app_type')
        user = User.objects.create_user(username=validated_data["phone_number"], **validated_data)

        # تخصیص گروه
        group = Group.objects.get(name='couriers' if app_type == 'courier' else 'senders')
        user.groups.add(group)
        user.save()

        return user





class PhoneNumberTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["phone_number"] = user.phone_number
        return token
