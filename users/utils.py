from django.contrib.auth.decorators import user_passes_test

def is_receptionist(user):
    return user.is_authenticated and user.user_type == 'receptionist'