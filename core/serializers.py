from rest_framework import serializers
from account.serializers.user import UserSerializer
from .models import LabService, CareGiver, CareGiverAppointment, LabServiceAppointment, TransactionCGService,\
TransactionLabService
from .constants import KHALTI, CASH


class LabServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabService
        fields = ["uuid", "name", "description"]


class CareGiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareGiver
        fields = ["uuid", "speciality", "languages", "ratings", "experience", "bio", "user"]

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        if request and request.method == "GET":
            fields['user'] = UserSerializer(context={"request": request})

        return fields

class BookAppointmentSerializer(serializers.Serializer):
    appointment_for = serializers.UUIDField()
    full_name = serializers.CharField(max_length=20)
    phone = serializers.CharField(max_length=14)
    address = serializers.CharField(max_length=50)
    start_date = serializers.DateField()
    end_date = serializers.DateField(required=False)
    description = serializers.CharField(max_length=100)
    payment_medium = serializers.ChoiceField(choices=(
        (KHALTI, KHALTI), (CASH, CASH)
    ))

    appt_for = None


    def validate(self, attrs):
        if isinstance(attrs['appointment_for'], CareGiver):
            self.appt_for = "Caregiver"
            if not attrs.get('end_date'):
                raise serializers.ValidationError("Please mention the end date !!")
        return attrs

    def validate_appointment_for(self, appointment_for):
        if CareGiver.objects.filter(uuid=appointment_for).exists():
            self.appt_for = "Caregiver"
            return CareGiver.objects.get(uuid=appointment_for)
        if LabService.objects.filter(uuid=appointment_for).exists():
            self.appt_for = "Labservice"
            return LabService.objects.get(uuid=appointment_for)
        raise serializers.ValidationError("Invalid caregiver or labservice id !!")

        


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
