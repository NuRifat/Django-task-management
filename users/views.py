from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from users.forms import RegisterForm, CustomRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(
                request, 'A Confirmation mail sent. Please check your email')
            return redirect('sign-in')
						##### Upto This ######
						
        else:
            print("Form is not valid")
    return render(request, 'registration/register.html', {"form": form})

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'registration/login.html', {
                'error': 'Invalid username or password'
            })
    return render(request, 'registration/login.html')

def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')