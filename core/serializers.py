from rest_framework import serializers
from account.serializers.user import UserSerializer
from .models import LabService, CareGiver, CareGiverAppointment, LabServiceAppointment, TransactionCGService,\
TransactionLabService


class LabServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabService
        fields = ["uuid", "name", "description"]


class CareGiverSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = CareGiver
        fields = ["uuid", "speciality", "languages", "ratings", "experience", "bio", "user"]

class CGAppointmentSerializer(serializers.ModelSerializer):
    caregiver = serializers.SlugRelatedField(slug_field="uuid", queryset=CareGiver.objects.all())
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    class Meta:
        model = CareGiverAppointment
        fields = ["uuid", "caregiver", "service", "start_date", "end_date"]

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        if request and request.method.lower() == "get":
            fields['user'] = UserSerializer()
        return fields

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['user'] = request.user
        return super().create(validated_data)


class CGTranxInitiateSer(serializers.Serializer):
    appointment = serializers.UUIDField()
    service = None

    def validate_appointment(self, appt):
        if CareGiverAppointment.objects.filter(uuid=appt).exists():
            self.service = "Caregiver"
            return CareGiverAppointment.objects.get(uuid=appt)
        if LabServiceAppointment.objects.filter(uuid=appt).exists():
            self.service = "Labservice"
            return LabServiceAppointment.objects.get(uuid=appt)
        raise serializers.ValidationError("Invalid appointment id !!")


class TranxVerifySer(serializers.Serializer):
    khalti_token = serializers.CharField(max_length=100)
    transaction_uuid = serializers.UUIDField()
    service = None

    def validate_transaction_uuid(self, uuid):
        if TransactionCGService.objects.filter(uuid=uuid).exists():
            self.service = "Caregiver"
            return TransactionCGService.objects.get(uuid=uuid)
        if TransactionLabService.objects.filter(uuid=uuid).exists():
            self.service = "Labservice"
            return TransactionLabService.objects.get(uuid=uuid)
        raise serializers.ValidationError("Invalid transaction id !!")


    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
