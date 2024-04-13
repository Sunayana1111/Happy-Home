from django import forms
from .models import CareGiver


class CaregiverForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        caregiver = CareGiver.objects.filter(user=user)
        if caregiver:
            caregiver = caregiver[0]
            cg_fields = ["speciality", "languages", "experience", "bio"]
            for field in cg_fields:
                self.fields[field].initial = getattr(caregiver, field)
        try:
            profile = user.userprofile
            self.fields["profile_picture"].initial = profile.profile_picture
        except:
            pass

    class Meta:
        model = CareGiver
        fields = ['speciality', "languages", "experience", "bio"]
