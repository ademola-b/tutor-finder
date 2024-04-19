from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views.generic import View

from . decorators import user_profile_checker, redirect_anonymous_user
# Create your views here.


@method_decorator(redirect_anonymous_user, name="get")
@method_decorator(user_profile_checker, name="get")
class DashboardView(View):
    template_name = 'dashboard.html'

    def get(self, request):
        return render(request, self.template_name, {})
    
