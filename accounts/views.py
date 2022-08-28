
from django.shortcuts import render, HttpResponse, redirect
from django.utils import timezone
from django.views import View
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib import messages


class SignupView(View):

    form_class = UserRegistrationForm
    template_name = 'accounts/signup.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            personal_id = form.cleaned_data['personal_id']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            full_name = form.cleaned_data['full_name']
            print(email)
            print(full_name)
            User.objects.create_user(personal_id, full_name, email, phone_number, password)
            messages.success(request, 'Your account has been created successfully', 'alert alert-success')
            return redirect('home:home')
        else:
            messages.error(request, 'BAD REQUEST.', 'alert alert-danger')
            return redirect('accounts:user_signup')


class LoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(request, personal_id=form.cleaned_data['personal_id'],
                                password=form.cleaned_data['password'])
            if user is not None:
                user.last_login = timezone.now()
                user.save()
                login(request, user)
                return redirect('home:home')
            else:
                messages.error(request, 'Invalid Username or Password', 'alert alert-danger')
        return render(request, self.template_name, {'form': form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('accounts:user_login')
