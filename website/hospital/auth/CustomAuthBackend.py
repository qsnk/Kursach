from django.contrib.auth.models import User
from .models import Patient

class AuthBackend:
    def authentificate(self, request, username, password):
        try:
            user = Patient.objects.get(username=username)
            success = user.check_password()
        except:
            pass