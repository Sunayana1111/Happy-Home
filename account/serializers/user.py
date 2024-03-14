from rest_framework import serializers
from django.contrib.auth.models import User, Group

from account.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', "email", "username", "password", "first_name", "last_name", "password2"]
    
    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        if request and request.method.lower() == "post":
            fields["gender"] = serializers.CharField(max_length=20)
            fields["age"] = serializers.IntegerField()
            fields["phone"] = serializers.CharField(max_length=20)
            fields["address"] = serializers.CharField(max_length=20)
            fields["role"] = serializers.CharField(max_length=10)
        return fields

    def create(self, validated_data):
        gender = validated_data.pop("gender")
        phone = validated_data.pop("phone")
        address = validated_data.pop("address")
        age = validated_data.pop("age")
        role = validated_data.pop("role")
        password2 = validated_data.pop('password2')
        user = super().create(validated_data)
        user.set_password(password2)
        user.save()
        UserProfile.objects.create(user=user, gender=gender, phone=phone, address=address, age=age)
        role = Group.objects.get(name=role)
        user.groups.add(role)
        return user