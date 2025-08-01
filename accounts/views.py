from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from .models import User

class RegisterView(View):
    template_name = 'register.html'

    def check_user_authentication(self):
        return True

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        data = request.POST
        name = data.get('name', '').strip()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        # Validation
        if not all([name, username, email, password, confirm_password]):
            messages.error(request, "All fields are required.")
            return redirect('accounts:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('accounts:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('accounts:register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('accounts:register')
        
        is_user_authenticated = self.check_user_authentication() # Email verification function!!
        if(is_user_authenticated):
            messages.success(request, "Registration successful!")
        
            try:
                User.objects.create_user(
                    username=username,
                    email=email,
                    name=name,
                    password=password
                )

                return redirect('dashboard:usr_dashboard')
            except Exception as e:
                messages.error(request, f"Registration failed: {str(e)}")
                return redirect('accounts:register')


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        # Clear any existing messages before rendering the login form
        storage = messages.get_messages(request)
        storage.used = True
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard:usr_dashboard')
        messages.error(request, "Invalid credentials.")
        return redirect('accounts:login')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('accounts:login')
