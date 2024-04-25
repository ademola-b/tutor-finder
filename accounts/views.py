from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View, CreateView, UpdateView

from finder.decorators import user_profile_checker, redirect_anonymous_user
from . forms import (LoginForm, SignUpForm, UserUpdateForm, 
                     TutorUpdateForm, TutorCredentialsForm)
from . models import Tutor, Student, TutorCredential, VerificationStatus
# Create your views here.

class LoginView(View):
    template_name = 'auth/login.html'
    
    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('finder:dashboard')
                else:
                    messages.error(request, "Account is not active, kindly contact the admin")
            else:
                messages.error(request, "Invalid username/password")
        else:
            messages.error(request, f"An error occurred: {form.errors.as_text()}")
        return render(request, self.template_name, {'form':form})

class RegisterView(CreateView):
    template_name = 'auth/register.html'
    
    def get(self, request):
        form = SignUpForm
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            # check_tutor = form.cleaned_data.get('is_tutor')
            form.save()
            messages.success(request, "Account Successfully created")
            return redirect("auth:login")
        else:
            messages.error(request, f"{form.errors.as_text()}")

        return render(request, self.template_name, {'form':form})

@method_decorator(redirect_anonymous_user, name="get")   
class ProfileUpdateView(UpdateView):
    template_name = 'auth/update_profile.html'
    form = UserUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.form(instance=request.user)
        return render(request, self.template_name, {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, instance=request.user)
        if form.is_valid():
            instance = form.save(commit=False)
            check_tutor = form.cleaned_data.get('is_tutor')
            try:
                if check_tutor:
                    instance.is_tutor = True
                    instance.save()
                    Tutor.objects.get_or_create(user = request.user)
                    messages.info(request, "kindly fill your information")
                    return redirect("auth:tutor_profile")
                else:
                    instance.save()
                    Student.objects.get_or_create(user=instance)
                    messages.success(request, "Profile Updated")
                    return redirect("finder:dashboard")
            except IntegrityError:
                messages.warning(request, "Error while updating form")
                return redirect("auth:login")
        else:
            messages.error(request, f"{form.errors.as_text()}")
        return render(request, self.template_name, {'form':form})

@method_decorator(redirect_anonymous_user, name="get")   
class TutorFormBView(UpdateView):
    template_name = 'auth/tutor_profile.html'
    form_class = TutorUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user.tutor)
        if form.is_valid():
            instance = form.save(commit=False)
            
            instance.isAvailable = True
            instance.save()
            messages.success(request, "Information Saved")
            return redirect("finder:dashboard")
        else:
            messages.error(request, f"{form.errors.as_text()}")
        return render(request, self.template_name, {'form':form})

@method_decorator(redirect_anonymous_user, name="get")
class TutorVerificationView(View):
    template_name = 'auth/verification.html'
    form_class = TutorCredentialsForm

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            unverified_tutors = Tutor.objects.filter(isVerified=False)
            context = {'tutors':unverified_tutors}
        else:
            try:
                form = self.form_class()
                doc = VerificationStatus.objects.filter(credential__tutor__user = request.user)
                status = Tutor.objects.get(user = request.user)
                context = {'form':form,'documents':doc, 'status':status}
            except Tutor.DoesNotExist:
                messages.warning(request, "Profile doesn't exist, update")
                return redirect("auth:update_profile")
        
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            tutor = Tutor.objects.get(user=request.user)
            rec = TutorCredential.objects.filter(tutor=tutor, document_name=form.cleaned_data.get('document_name')).first()
            if rec:
                messages.warning(request, "Selected Document already uploaded")
                return redirect(reverse('auth:verification'))
            else:
                instance = form.save(commit=False)
                instance.tutor = tutor
                instance.save()
                VerificationStatus.objects.create(credential=instance)
                messages.success(request, "Document Succesfully Uploaded")
                return redirect(reverse('auth:verification'))
        else:
            messages.warning(request, f"{form.errors.as_text()}")
        return render(request, self.template_name, {'form':form})


def logout_request(request):
    logout(request)
    return redirect('auth:login')


