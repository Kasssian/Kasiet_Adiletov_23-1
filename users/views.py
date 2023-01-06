from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from users.forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import FormView, CreateView


class LoginCBV(LoginView, FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = '/products/'

    def get_context_data(self, **kwargs):
        return {
            'form': kwargs['form']
        }

    def get(self, request, *args):
        return render(request, self.template_name, self.get_context_data(
            form=self.form_class
        ))

    def post(self, request, *args, **kwargs):
        form = LoginForm(data=request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'),
            )
            if user:
                login(request, user=user)
                return redirect(self.success_url)
            else:
                form.add_error('username', 'Не правильно введён пароль или логин.')
        return render(request, self.template_name, self.get_context_data(
            form=self.form_class
        ))


class LogoutCBV(LogoutView, FormView):
    success_url = '/products/'

    def get(self, request):
        logout(request)
        return redirect(self.success_url)


class RegisterCBV(CreateView, FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = '/products/'

    def get_context_data(self, **kwargs):
        return {
            'form': kwargs['form']
        }

    def get(self, request, *args):
        return render(request, self.template_name, self.get_context_data(
            form=self.form_class
        ))

    def post(self, request, *args, **kwargs):
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            if form.cleaned_data.get('password_1') == form.cleaned_data.get('password_2'):
                user = User.objects.create_user(
                    username=form.cleaned_data.get('username'),
                    password=form.cleaned_data.get('password_2'),
                )
                login(request, user)
                return redirect('/products/')
            else:
                form.add_error('password_2', 'Пароли не совпадают.')

        return render(request, self.template_name, self.get_context_data(
            form=self.form_class
        ))
