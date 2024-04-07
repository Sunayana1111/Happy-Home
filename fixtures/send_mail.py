import os
import sys
import django

sys.path.insert(0, os.path.join(sys.path[0], '..'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'happy_home.settings')

django.setup()
from django.core.mail import send_mail
from django.conf import settings


send_mail("Test", "Hello", settings.DEFAULT_FROM_EMAIL, settings.TO_EMAIL)
print("success!!")
