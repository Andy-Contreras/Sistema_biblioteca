# decorators.py

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

def no_es_lector(user):
    # Verifica si el usuario no es un lector
    if user.is_authenticated and user.is_reader():
        return False
    return True
