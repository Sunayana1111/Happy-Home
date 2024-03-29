from django.db import models
from django.contrib.auth.models import User

from commons.models import BaseModel


class UserProfile(BaseModel):
    gender_choices = (
        ("Male", "MALE"),
        ("Female", "FEMALE"),
        ("Other", "OTHER"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    gender = models.CharField(choices=gender_choices, max_length=20)
    phone = models.CharField(max_length=14)
    address = models.CharField(max_length=50)
    profile_picture = models.FileField(upload_to="profile_pictures", null=True, blank=True)

    def __str__(self) -> str:
        return f"Profile of {self.user.username}"