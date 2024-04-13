import random
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def generate_random_key(size, alpha_numeric=False):
    letters = "1234567890"
    if alpha_numeric:
        letters += "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
    random_key = ""
    for _ in range(size):
        random_key += random.choice(letters)
    return random_key


def send_template_email(user, subject='', template_name='', context=None):
    template_name = "email/invoice.html"
    message = render_to_string(template_name=template_name, context=context)
    email = EmailMessage(subject=f'Happy Home-{subject}', from_email=getattr(settings, "DEFAULT_FROM_EMAIL"),
                         body=message, to=[settings.TO_EMAIL, user.email, "naween321@gmail.com"])
    email.content_subtype = "html"
    email.send()
