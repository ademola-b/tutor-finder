from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView
from . forms import LoginForm, SignUpForm
from . models import Tutor, Student
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
            check_tutor = form.cleaned_data.get('is_tutor')
            instance = form.save()
            if check_tutor:
                Tutor.objects.create(user = instance)
                messages.success(request, "Account Successfully created, kindly upload your credentials for verification")
                return redirect("auth:login")
            else:
                Student.objects.create(user = instance)
                messages.success(request, "Account Successfully created, kindly update your profile")
                return redirect("auth:login")
        else:
            messages.error(request, f"{form.errors.as_text()}")

        return render(request, self.template_name, {'form':form})
    




