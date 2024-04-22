from django.contrib import messages
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views.generic import View
from accounts.models import Tutor, Student

from . forms import BookSessionForm
from . models import SessionBook


from . decorators import user_profile_checker, redirect_anonymous_user
# Create your views here.


@method_decorator(redirect_anonymous_user, name="get")
@method_decorator(user_profile_checker, name="get")
class DashboardView(View):
    template_name = 'dashboard.html'

    def get(self, request):
        if request.user.is_tutor:
            sessions = SessionBook.objects.filter(tutor = request.user.tutor)
        else:
            sessions = SessionBook.objects.filter(student = request.user.student)

        return render(request, self.template_name, {'sessions':sessions})

class BookSessionView(View):
    template_name = 'finder/available_tutors.html'
    form_class = BookSessionForm
    tutors = Tutor.objects.filter(isAvailable=True, isVerified=True)

    def get(self, request):
        avail_tutors = self.tutors
        form = self.form_class()
        return render(request, self.template_name, {'avail_tutors':avail_tutors, 'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if 'selectedTutor' in request.POST:
                instance.tutor = Tutor.objects.get(tutor_id = request.POST['selectedTutor'])
                instance.student = Student.objects.get(user=request.user)
                instance.save()
                messages.success(request, "Session successfully booked, kindly wait for the tutor's response")
                return redirect("finder:dashboard")        
        else:
            messages.warning(request, f"{form.errors.as_text()}")
            return render(request, self.template_name, {'avail_tutors':self.tutors, 'form':form})
    
