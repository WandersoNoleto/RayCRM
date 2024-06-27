from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from .utils import is_receptionist

def receptionist_required(function=None):
    actual_decorator = user_passes_test(
        lambda user: is_receptionist(user),
        login_url='/login/'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
