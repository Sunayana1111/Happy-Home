from rest_framework import serializers
from account.serializers.user import UserSerializer
from .models import LabService, CareGiver


class LabServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabService
        fields = ["uuid", "name", "description"]


class CareGiverSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = CareGiver
        fields = ["uuid", "speciality", "languages", "ratings", "experience", "bio", "user"]

class ApplyCareGivingSerializer(serializers.Serializer):
    caregiver = serializers.IntegerField()
