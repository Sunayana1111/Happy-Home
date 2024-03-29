from rest_framework import serializers
from django.contrib.auth.models import User

from account.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["age", "gender", "phone", "address", "profile_picture"]


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', "email", "username", "first_name", "last_name", "password", "password2", "profile"]
        extra_kwargs = {
            "password":{
                "write_only": True
            }
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Passwords didn't match")
        return attrs
    
    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        if request and request.method.lower() == "post":
            fields["gender"] = serializers.CharField(max_length=20)
            fields["age"] = serializers.IntegerField()
            fields["phone"] = serializers.CharField(max_length=20)
            fields["address"] = serializers.CharField(max_length=20)
        return fields

    def create(self, validated_data):
        gender = validated_data.pop("gender")
        phone = validated_data.pop("phone")
        address = validated_data.pop("address")
        age = validated_data.pop("age")
        password2 = validated_data.pop('password2')
        user = super().create(validated_data)
        user.set_password(password2)
        user.save()
        UserProfile.objects.create(user=user, gender=gender, phone=phone, address=address, age=age)
        return user
    
    def get_profile(self, obj):
        try:
            profile = obj.userprofile
        except:
            return {}
        return UserProfileSerializer(profile).data
