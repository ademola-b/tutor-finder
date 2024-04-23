from typing import Any
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.query import QuerySet
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DeleteView, UpdateView
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
            sessions = SessionBook.objects.filter(tutor = request.user.tutor, status = "ongoing")
        else:
            sessions = SessionBook.objects.filter(student = request.user.student, status="ongoing")

        return render(request, self.template_name, {'sessions':sessions})

@method_decorator(redirect_anonymous_user, name="get")
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
                messages.success(request, "Session successfully requested, kindly wait for the tutor's response")
                return redirect("finder:pending_session")        
        else:
            messages.warning(request, f"{form.errors.as_text()}")
            return render(request, self.template_name, {'avail_tutors':self.tutors, 'form':form})


@method_decorator(redirect_anonymous_user, name="get")
class PendingTutorSession(ListView):
    model = SessionBook
    template_name = "finder/pending_requests.html"
    context_object_name = "requests"

    def get_queryset(self) -> QuerySet[Any]:
        user = self.request.user
        if user.is_tutor:
            return SessionBook.objects.filter(tutor=user.tutor, status="pending")
        else:
            return SessionBook.objects.filter(student=user.student, status="pending")

@method_decorator(redirect_anonymous_user, name="get")
class DeletePendingSession(DeleteView, SuccessMessageMixin):
    model = SessionBook
    success_url = reverse_lazy('finder:pending_session')
    success_message = "Request Successfully Deleted"

class PendingSessionAction(UpdateView):
    model = SessionBook
    fields = ['status']
    success_url = reverse_lazy("finder:pending_session")
    template_name = "finder/pending_requests.html"
    
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if 'accept' in request.POST:
            session = SessionBook.objects.get(session_id=pk)
            session.status = "ongoing"
            session.save()
            messages.success(request, "Tutor session approved, and session has started.")
            return redirect(self.success_url)
        elif 'reject' in request.POST:
            session = SessionBook.objects.get(session_id=pk)
            session.status = "rejected"
            session.save()
            messages.success(request, "Tutor session rejected, and cannot be reversed.")
            return redirect(self.success_url)


        
    
