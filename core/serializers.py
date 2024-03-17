from rest_framework import serializers


class ApplyCareGivingSerializer(serializers.Serializer):
    caregiver = serializers.IntegerField()
