from typing import Any
from django.core.serializers import serialize
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View, CreateView, UpdateView, ListView, DetailView

from finder.decorators import user_profile_checker, redirect_anonymous_user
from . forms import (LoginForm, SignUpForm, UserUpdateForm, 
                     TutorUpdateForm, TutorCredentialsForm,
                     UserForm, TutorForm, StudentForm)
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
                rec.document_name = form.cleaned_data.get('document_name')
                rec.document = form.cleaned_data.get('document')
                rec.save()
                messages.warning(request, "Document Updated")
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

@method_decorator(redirect_anonymous_user, name="get")
class VerifyTutorView(View):
    template_name = "auth/verify-tutor.html"

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        docs = VerificationStatus.objects.filter(credential__tutor__tutor_id = pk, isVerified=False)
        tutor = Tutor.objects.get(tutor_id = pk)
        return render(request, self.template_name, {'docs':docs, 'tutor':tutor})
    
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        docs = VerificationStatus.objects.filter(credential__tutor__tutor_id=pk, isVerified=False)
        tutor = Tutor.objects.get(tutor_id=pk)

        # Create a dictionary to store the VerificationStatus instances for each document type
        verification_status = {document_name: None for document_name, _ in TutorCredential.Credential.choices}

        # Populate the dictionary with the VerificationStatus instances
        for doc in docs:
            verification_status[doc.credential.document_name] = doc
        
        print(f"verify: {verification_status}")

        if 'submit' in request.POST:
            verify_stat = {document_name: status_instance for document_name, status_instance in verification_status.items() if status_instance is not None}
            for document_name, status_instance in verify_stat.items():
                checkbox_name = f'{document_name}'
                reason_name = f'reason_{document_name.lower()}'

                if checkbox_name in request.POST:
                    # Document checkbox is checked, update isVerified to True
                    status_instance.isVerified = True
                    status_instance.rejection_reason = "accepted"
                else:
                    # Document checkbox is not checked, update rejection reason if provided
                    if reason_name in request.POST and request.POST[reason_name] != '':
                        status_instance.rejection_reason = request.POST[reason_name]
                    elif reason_name in request.POST and request.POST[reason_name] == '':
                        messages.warning(request, f"State why the {document_name} is not being accepted")
                        return redirect("auth:verify_tutor", pk)
                
                status_instance.admin = request.user
                status_instance.save()
                     
            #update verification tag
            verification_stat = {document_name: None for document_name, _ in TutorCredential.Credential.choices}
            docObjs = VerificationStatus.objects.filter(credential__tutor__tutor_id = pk)
            
            for doc in docObjs:
                verification_stat[doc.credential.document_name] = doc.isVerified
            
            all_verified = all(status is not None and status for status in verification_stat.values())
            if all_verified:
                tutor.isVerified = True
                tutor.save()
                # messages.info(request, "Tutor has been verified")
            
            messages.info(request, "Tutor's credentials has been assessed")
            return redirect("auth:verification")

        return render(request, self.template_name, {'docs': docs, 'tutor': tutor})

    
    # def post(self, request, *args, **kwargs):
    #     print(request.POST)
    #     pk = self.kwargs.get('pk')
    #     docs = VerificationStatus.objects.filter(credential__tutor__tutor_id = pk, isVerified=False)
    #     tutor = Tutor.objects.get(tutor_id = pk)

    #     ID = VerificationStatus.objects.filter(credential__tutor__tutor_id=pk, credential__document_name='ID').first()
    #     CV = VerificationStatus.objects.filter(credential__tutor__tutor_id=pk, credential__document_name='CV').first()
    #     cert = VerificationStatus.objects.filter(credential__tutor__tutor_id=pk, credential__document_name='CERTIFICATE').first()
        
    #     if 'submit' in request.POST:
    #         if 'ID' in request.POST:
    #             ID.isVerified = True
    #             ID.rejection_reason = "accepted"
    #         else:
    #             if 'reason_ID' in request.POST:
    #                 if request.POST['reason_ID'] == '':
    #                     messages.warning(request, "state why the ID is not being accepted")
    #                     return redirect("auth:verify_tutor", pk)
    #                 else:
    #                     ID.rejection_reason = request.POST['reason_ID']
                
    #         if 'CV' in request.POST:
    #             CV.isVerified = True
    #             CV.rejection_reason = "accepted"
    #         else:
    #             if 'reason_CV' in request.POST:
    #                 if request.POST['reason_CV'] == '':
    #                     messages.warning(request, "state why the CV is not being accepted")
    #                     return redirect("auth:verify_tutor", pk)
    #                 else:
    #                     CV.rejection_reason = request.POST['reason_CV']
            
    #         if 'CERTIFICATE' in request.POST:
    #             cert.isVerified = True
    #             cert.rejection_reason = "accepted"
    #         else:
    #             if 'reason_CERTIFICATE' in request.POST:
    #                 if request.POST['reason_CERTIFICATE'] == '':
    #                     messages.warning(request, "state why the certificate is not being accepted")
    #                     return redirect("auth:verify_tutor", pk)
    #                 else:
    #                     cert.rejection_reason = request.POST['reason_CERTIFICATE']
    #         ID.save()
    #         CV.save()
    #         cert.save()

    #         #update verification tag
    #         verification_status = {doc_status: None for doc_status, _ in TutorCredential.Credential.choices}
    #         docObjs = VerificationStatus.objects.filter(credential__tutor__tutor_id = pk)
            
    #         for doc in docObjs:
    #             verification_status[doc.credential.document_name] = doc.isVerified
            
    #         all_verified = all(status is not None and status for status in verification_status.values())
    #         if all_verified:
    #             tutor.isVerified = True
    #             tutor.save()



    #         # if ID and CV and cert and ID.isVerified and CV.isVerified and cert.isVerified:
    #         #     tutor.isVerified = True
    #         #     tutor.save()

                
    #     return render(request, self.template_name, {'docs':docs, 'tutor':tutor})

@method_decorator(redirect_anonymous_user, name="get")
class ProfileView(View):
    template_name = "auth/profile.html"
    user_form = UserForm
    form2 = TutorForm
    student_form = StudentForm

    def get(self, request):
        form = self.user_form(instance=request.user)
        context = {'form':form}
        if request.user.is_tutor:
            form2 = self.form2(instance=request.user.tutor)
        else:
            form2 = self.student_form(instance=request.user.student)

        context['form2'] = form2
        user_details = get_user_model().objects.get(user_id = request.user.user_id)
        context['user_details'] = user_details
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.user_form(request.POST, request.FILES, instance=request.user)
        if request.user.is_tutor:
            form2 = self.tutor_form(request.POST, instance=request.user.tutor)
        else:
            form2 = self.student_form(request.POST, instance=request.user.student)
        print(request.POST)
        if 'user' in request.POST:
            if form.is_valid():
                form.save()
            else:
                messages.warning(request, f"{form.errors.as_text()}")
        
        if 'tut' in request.POST:
            if form2.is_valid():
                form2.save()
            else:
                messages.warning(request, f"{form.errors.as_text()}")

        messages.success(request, "Profile successfully updated")
        return redirect(reverse("auth:profile"))

@method_decorator(redirect_anonymous_user, name="get")
class UsersList(ListView):
    model = get_user_model()
    template_name = "users.html"
    context_object_name = "users"

def get_users(request):
    type = request.GET.get('user_type')
    if type == 'student':
        users = get_user_model().objects.filter(is_tutor=False)
    elif type == 'tutor':
        users = get_user_model().objects.filter(is_tutor=True)
    else:
        users = get_user_model().objects.all()

    # convert retrieved data to json
    serialized_user = serialize('json', users)
    return JsonResponse(serialized_user, safe=False)

@method_decorator(redirect_anonymous_user, name="get")
class UserDetail(DetailView):
    template_name = "user-profile.html"
    context_object_name = "detail"

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user = get_object_or_404(get_user_model(), user_id=pk)
        try:
            if user.is_tutor:
                obj = Tutor.objects.get(user=user)
            else:
                obj = Student.objects.get(user=user)
            return obj
        except:
            messages.error(self.request, "User Details Not Found")





def logout_request(request):
    logout(request)
    return redirect('auth:login')


