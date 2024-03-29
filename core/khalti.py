from django.conf import settings


class KhaltiPayment:
    transaction_verify_url = "https://khalti.com/api/v2/payment/verify/"
    secret_key = getattr(settings, 'KHALTI_SECRET_KEY', "")
