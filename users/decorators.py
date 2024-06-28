from django.core.exceptions import PermissionDenied
from functools import wraps
from users.models import User
from django.shortcuts import redirect

def user_is_clinic(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'clinic':
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrapped_view

def user_is_doctor(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'doctor':
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrapped_view


def user_is_receptionist(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            try:
                db_user = User.objects.get(username=user.username)
                if db_user.user_type == 'receptionist':
                    return view_func(request, *args, **kwargs)
                else:
                    raise PermissionDenied
            except User.DoesNotExist:
                raise PermissionDenied
            except Exception as e:
                raise PermissionDenied
        else:
            return redirect('login') 
    return _wrapped_view

def user_is_partner_optic(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'partner_optic':
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return _wrapped_view
