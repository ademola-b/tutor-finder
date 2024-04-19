from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.shortcuts import redirect
from accounts.models import Tutor, Student


def redirect_anonymous_user(func):
    def wrapper_func(request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            messages.warning(request, 'You are not authenticated, kindly login')
            return redirect('auth:login')
        return func(request, *args, **kwargs)
    return wrapper_func

def user_profile_checker(func):
    def wrapper_func(request, *args, **kwargs):
        user = request.user
        try:
            user = Tutor.objects.get(user=user)
            if not user.isVerified:
                messages.warning(request, "You are not verified yet")
                return redirect('auth:verification')
            return func(request, *args, **kwargs)
        except Tutor.DoesNotExist:
            try:
                user = Student.objects.get(user=user)
                return func(request, *args, **kwargs)
            except Student.DoesNotExist:
                messages.warning(request, "Kindly update your profile")
            return redirect('auth:update_profile') 
    return wrapper_func